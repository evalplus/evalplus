import json
import os
from abc import ABC, abstractmethod
from typing import List
from warnings import warn

# Communism
os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/JawTitan/huggingface/")

import openai

try:
    import anthropic

    from evalplus.gen.util import anthropic_request
except ImportError:
    warn("Anthropic decoder will not work. Fix by `pip install anthropic`")

# mistral.ai
try:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
except ImportError:
    warn("MistralAI decoder will not work. Fix by `pip install mistralai`")

import torch
from stop_sequencer import StopSequencer
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

try:
    from vllm import LLM, SamplingParams
except ImportError:
    warn("VLLM decoder will not work. Fix by `pip install vllm`")

from evalplus.gen.util import openai_request

EOS = [
    "<|endoftext|>",
    "<|endofmask|>",
    "</s>",
    "\nif __name__",
    "\ndef main(",
    "\nprint(",
]


class DecoderBase(ABC):
    def __init__(
        self,
        name: str,
        batch_size: int = 1,
        temperature: float = 0.8,
        max_new_tokens: int = 512,
        direct_completion: bool = True,
        dtype: str = "bfloat16",  # default
        trust_remote_code: bool = False,
        dataset: str = None,
    ) -> None:
        print("Initializing a decoder model: {} ...".format(name))
        self.name = name
        self.batch_size = batch_size
        self.temperature = temperature
        self.eos = EOS
        self.skip_special_tokens = False
        self.max_new_tokens = max_new_tokens
        self.direct_completion = direct_completion
        self.dtype = dtype
        self.trust_remote_code = trust_remote_code

        if direct_completion:
            if dataset.lower() == "humaneval":
                self.eos += ["\ndef ", "\nclass ", "\nimport ", "\nfrom ", "\nassert "]
            elif dataset.lower() == "mbpp":
                self.eos += ['\n"""', "\nassert"]

    @abstractmethod
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        pass

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class VLlmDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)

        kwargs = {
            "tensor_parallel_size": int(os.getenv("VLLM_N_GPUS", "1")),
            "dtype": self.dtype,
            "trust_remote_code": self.trust_remote_code,
        }

        self.llm = LLM(model=name, max_model_len=2048, **kwargs)

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"
        batch_size = min(self.batch_size, num_samples)

        vllm_outputs = self.llm.generate(
            [prompt] * batch_size,
            SamplingParams(
                temperature=self.temperature,
                max_tokens=self.max_new_tokens,
                top_p=0.95 if do_sample else 1.0,
                stop=self.eos,
            ),
            use_tqdm=False,
        )

        gen_strs = [x.outputs[0].text.replace("\t", "    ") for x in vllm_outputs]
        return gen_strs


# chatml format
class ChatML(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""<|im_start|>system
You are an intelligent programming assistant to produce Python algorithmic solutions<|im_end|>
<|im_start|>user
Can you complete the following Python function?
```python
{prompt}
```
<|im_end|>
<|im_start|>assistant
```python
"""
        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class Mixtral(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""<s>[INST]Please complete and solve the following Python function in a markdown block.
```python
{prompt}
```
[/INST]
```python
"""
        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class CodeLlamaInstruct70B(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""'<s>Source: system

 You are a helpful and honest code assistant expert in Python. Please, provide all answers to programming questions in Python.
 <step> Source: user

 Provide a self-contained Python script that solves the following problem:
```python
{prompt}
```
 <step> Source: assistant

 Here is a Python script that solves the problem:
```python
"""

        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class CodeLlamaInstructSmall(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""[INST] Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
```python
{prompt}
```
[/INST]
```python
"""

        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


# zyte format
class Zyte(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""<|system|>You are an intelligent programming assistant to produce Python algorithmic solutions</s>
<|user|>Can you complete the following Python function?
```python
{prompt}
```
</s>
<|assistant|>
```python
"""
        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class OpenChat(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""GPT4 Correct User: Can you complete the following Python function?
```python
{prompt}
```
<|end_of_turn|>GPT4 Correct Assistant:
```python
"""
        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class Solar(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be greater than 0!"

        input = f"""<s> ### User:
Can you solve and complete the Python function below?
```python
{prompt}
```

### Assistant:
Sure!
```python
"""
        return VLlmDecoder.codegen(self, input, do_sample, num_samples)


class Alpaca(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes request.

### Instruction:
Create a Python script for this problem:
{prompt}

### Response:
```python
"""

        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class WhiteRabbitNeo(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""You code like a superhero!
USER:
Create a Python script to solve this problem:
```python
{prompt}
```
ASSISTANT:
```python
"""

        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class HFTorchDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        kwargs = {}
        kwargs["device_map"] = "auto"
        kwargs["trust_remote_code"] = self.trust_remote_code
        # string to torch dtype
        kwargs["torch_dtype"] = getattr(torch, self.dtype)
        self.skip_special_tokens = True

        print(f"{kwargs = }")

        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(name, **kwargs)
        self.model = self.model.to(self.device)

    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").to(
            self.device
        )
        kwargs = {}
        if do_sample:
            kwargs["top_p"] = 0.95
            kwargs["temperature"] = self.temperature

        stop_sequencer = StopSequencer(
            self.model,
            model_type="causal",  # or seq2seq
            tokenizer=self.tokenizer,
        )

        model = stop_sequencer.register_stop_texts(
            stop_texts=self.eos,
            input_length=input_tokens.size(-1),
        )

        outputs = model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            do_sample=do_sample,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.eos_token_id,
            **kwargs,
        )

        gen_strs = self.tokenizer.batch_decode(
            outputs[:, input_tokens.size(-1) :],
            skip_special_tokens=self.skip_special_tokens,
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index].replace("\t", "    "))
        return outputs


class DeepSeekInstruct(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Please complete the following Python function in a markdown style code block:
```python
{prompt}
```
### Response:
```python
"""

        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class Magicoder(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.

@@ Instruction
{prompt}

@@ Response
```python
        """

        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class OpenAIChatDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.client = openai.OpenAI()

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        batch_size = min(self.batch_size, num_samples)

        # construct prompt
        fmt = "json_object" if self.name == "gpt-4-1106-preview" else "text"
        if fmt == "json_object":
            message = r'Please complete the following code snippet by generating JSON like {"code": ""}'
        else:
            message = r"Please generate code to complete the following problem:"

        message += f"\n```python\n{prompt.strip()}\n```"

        ret = openai_request.make_auto_request(
            self.client,
            message=message,
            model=self.name,
            max_tokens=self.max_new_tokens,
            temperature=self.temperature,
            n=batch_size,
            response_format={"type": fmt},
        )

        outputs = []
        for item in ret.choices:
            content = item.message.content
            # if json serializable
            if fmt == "json_object":
                try:
                    json_data = json.loads(content)
                    if json_data.get("code", None) is not None:
                        outputs.append(prompt + "\n" + json_data["code"])
                        continue

                    print(f"'code' field not found in: {json_data}")
                except Exception as e:
                    print(e)
            outputs.append(content)

        return outputs


class MistralChatDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        kwargs = {}
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
            kwargs["top_p"] = 0.95
            kwargs["temperature"] = self.temperature
        else:
            self.temperature = 0

        batch_size = min(self.batch_size, num_samples)

        outputs = []
        for _ in range(batch_size):
            ret = self.client.chat(
                model=self.name,
                messages=[
                    ChatMessage(
                        role="user",
                        content="Please generate code to solve the following problem in a Python markdown block:"
                        + f"\n```python\n{prompt.strip()}\n```",
                    )
                ],
                max_tokens=self.max_new_tokens,
                **kwargs,
            )

            outputs.append(ret.choices[0].message.content)

        return outputs


class AnthropicDecoder(DecoderBase, ABC):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))


class AnthropicMessageDecoder(AnthropicDecoder):
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"

        batch_size = min(self.batch_size, num_samples)
        if not do_sample:
            assert batch_size == 1, "Sampling only supports batch size of 1"

        outputs = []
        for _ in range(batch_size):
            message = anthropic_request.make_auto_request(
                client=self.client,
                model=self.name,
                messages=[
                    {
                        "role": "user",
                        "content": "Please generate code to complete the following problem wrapped in a Python markdown block:"
                        + f"\n```python\n{prompt.strip()}\n```\n",
                    }
                ],
                max_tokens=self.max_new_tokens,
                temperature=self.temperature,
                stop_sequences=["\n```\n", "\nif "],
            )
            outputs.append(message.content[0].text)

        return outputs


class IncoderDecoder(HFTorchDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.infill_ph = "<|mask:0|>"
        self.extra_end = "<|mask:1|><|mask:0|>"
        self.extra_eos = [
            "<|endofmask|>",
            "<|/ file",
            "</cell>",
            "</text>",
            "</code>",
            "<|",
            "</CODE>",
        ]
        self.eos = self.eos + self.extra_eos

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = prompt + self.infill_ph + self.extra_end
        return HFTorchDecoder.codegen(self, input, do_sample, num_samples)


class Codegen2Decoder(HFTorchDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.infill_ph = "<mask_1>"
        # taken from: https://huggingface.co/Salesforce/codegen2-16B
        self.extra_end = "<|endoftext|><sep><mask_1>"
        self.extra_eos = ["<eom>"]
        self.eos = self.eos + self.extra_eos

    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = prompt + self.infill_ph + self.extra_end
        return HFTorchDecoder.codegen(self, input, do_sample, num_samples)


class Speechless(HFTorchDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        if "uukuguy/speechless-coding-7b-16k-tora" == name:
            self.extra_eos = ["</s>"]
        elif "uukuguy/speechless-coder-ds-6.7b" == name:
            self.extra_eos = ["<｜end▁of▁sentence｜>"]
        else:
            raise ValueError(f"Invalid model name: {name}")
        self.eos = self.eos + self.extra_eos


class CodeT5P(DecoderBase):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        assert name in {
            "Salesforce/codet5p-2b",
            "Salesforce/codet5p-6b",
            "Salesforce/codet5p-16b",
            "Salesforce/instructcodet5p-16b",
        }
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            name,
            trust_remote_code=True,  # False for 220m and 770m models
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
        self.model.eval()
        self.model.to(self.device)

        self.skip_special_tokens = True

    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = prompt.replace("    ", "\t")
        return HFTorchDecoder.codegen(self, prompt, do_sample, num_samples)


class Code(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""This is a conversation with your helpful AI assistant. AI assistant can generate Python Code along with necessary explanation.

Context
You are a helpful AI assistant.

USER:
```python
{prompt}
```
ASSISTANT:
```python
"""
        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class XwinCoder(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""<system>: You are an AI coding assistant that helps people with programming. Write a response that appropriately completes the user's request.
<user>: Complete the following code for me and return a fully runable code.
```python
{prompt}
```
<AI>:
```python
"""
        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


class OpenCodeInterpreterDecoder(HFTorchDecoder):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.skip_special_tokens = True
        self.eos += ["<|EOT|>", "\n```\n", "\nif "]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.

@@ Instruction
Here is a Python programming problem to solve:
```python
{prompt}
```
Please implement this function in a Python markdown code block starting with "```python" and follow the function/input/output formats.

@@ Response
"""
        return HFTorchDecoder.codegen(self, prompt, do_sample, num_samples)


class CodeGemma(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["direct_completion"] = False
        super().__init__(name, **kwargs)
        self.eos += ["\n```"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = f"""### Instruction
{prompt}
### Response
"""
        return VLlmDecoder.codegen(self, prompt, do_sample, num_samples)


def make_model(
    name: str, batch_size: int = 1, temperature: float = 0.8, dataset: str = None
):
    if name == "codegen-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-2B-mono",
            temperature=temperature,
            dtype="float16",
            dataset=dataset,
        )
    elif name == "codegen-6b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-6B-mono",
            temperature=temperature,
            dtype="float16",
            dataset=dataset,
        )
    elif name == "codegen-16b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-16B-mono",
            temperature=temperature,
            dtype="float16",
            dataset=dataset,
        )
    elif name == "codegen2-1b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-1B",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "codegen2-3b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-3_7B",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "codegen2-7b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-7B",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "codegen2-16b":
        warn(
            "codegen2-16b checkpoint is `unfinished` at this point (05/11/2023) according to their paper. "
            "So it might not make sense to use it."
        )
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-16B",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "polycoder":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="NinedayWang/PolyCoder-2.7B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "santacoder":
        return VLlmDecoder(
            batch_size=batch_size,
            name="bigcode/santacoder",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "incoder-1b":
        return IncoderDecoder(
            batch_size=batch_size,
            name="facebook/incoder-1B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "incoder-6b":
        return IncoderDecoder(
            batch_size=batch_size,
            name="facebook/incoder-6B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "stablelm-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="StabilityAI/stablelm-base-alpha-7b",
            temperature=temperature,
            dataset=dataset,
        )
    elif name.startswith("gpt-3.5-") or name.startswith("gpt-4-"):
        return OpenAIChatDecoder(
            batch_size=batch_size,
            name=name,
            temperature=temperature,
            direct_completion=False,
        )
    elif name.startswith("claude"):
        return AnthropicMessageDecoder(
            batch_size=batch_size,
            name=name,
            temperature=temperature,
            direct_completion=False,
            dataset=dataset,
        )
    elif name == "gptneo-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="EleutherAI/gpt-neo-2.7B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "gpt-j":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="EleutherAI/gpt-j-6B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name.startswith("starcoder"):
        return HFTorchDecoder(
            batch_size=batch_size,
            name=f"bigcode/{name}",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "codet5p-2b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-2b",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "codet5p-6b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-6b",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "codet5p-16b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-16b",
            temperature=temperature,
            dataset=dataset,
        )
    elif name.startswith("code-llama-"):
        if name.endswith("instruct"):
            nb = name.split("-")[2]
            assert nb.endswith("b")
            if nb == "70b":
                return CodeLlamaInstruct70B(
                    batch_size=batch_size,
                    name=f"codellama/CodeLlama-70B-Instruct-hf",
                    temperature=temperature,
                    direct_completion=False,
                )
            else:
                return CodeLlamaInstructSmall(
                    batch_size=batch_size,
                    name=f"codellama/CodeLlama-{nb}-Instruct-hf",
                    temperature=temperature,
                    direct_completion=False,
                )
        assert name.endswith("b")
        nb = name.split("-")[-1]

        # Multi-lingual
        if name.startswith("code-llama-multi"):
            return VLlmDecoder(
                batch_size=batch_size,
                name=f"codellama/CodeLlama-{nb}-hf",
                temperature=temperature,
                dataset=dataset,
            )

        # Python only
        return VLlmDecoder(
            batch_size=batch_size,
            name=f"codellama/CodeLlama-{nb}-Python-hf",
            temperature=temperature,
            dataset=dataset,
        )
    elif name.startswith("deepseek-coder"):
        import re

        # format deepseek-coder-{nb}b-{base|instruct}-[v{version}]
        pattern = re.compile(r"deepseek-coder-(\d+\.?\d*)b(.*)")
        matches = pattern.findall(name)[0]
        nb = float(matches[0])
        if nb.is_integer():
            nb = int(nb)

        if "instruct" in name:
            # if version is specified, use it
            version = matches[1].split("-")[-1]
            version_suffix = f"-{version}" if version.startswith("v") else ""
            return DeepSeekInstruct(
                batch_size=batch_size,
                name=f"deepseek-ai/deepseek-coder-{nb}b-instruct{version_suffix}",
                temperature=temperature,
                direct_completion=False,
            )
        else:
            version = matches[1].split("-")[-1]
            version_suffix = f"-{version}" if version.startswith("v") else ""
            return VLlmDecoder(
                batch_size=batch_size,
                name=f"deepseek-ai/deepseek-coder-{nb}b-base{version_suffix}",
                temperature=temperature,
                dataset=dataset,
            )
    elif name == "magicoder-s-ds-6.7b":
        return Magicoder(
            batch_size=batch_size,
            name="ise-uiuc/Magicoder-S-DS-6.7B",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "magicoder-s-cl-7b":
        return Magicoder(
            batch_size=batch_size,
            name="ise-uiuc/Magicoder-S-CL-7B",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "wizardcoder-33b-v1.1":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-33B-V1.1",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "wizardcoder-34b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-Python-34B-V1.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "wizardcoder-15b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-15B-V1.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "wizardcoder-7b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-Python-7B-V1.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "mistral-7b-codealpaca":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Nondzu/Mistral-7B-codealpaca-lora",
            temperature=temperature,
            dtype="float16",
            dataset=dataset,
        )
    elif name == "zephyr-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="HuggingFaceH4/zephyr-7b-beta",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "codebooga-34b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="oobabooga/CodeBooga-34B-v0.1",
            temperature=temperature,
            dtype="float16",
            dataset=dataset,
        )
    elif name == "code-13b":
        return Code(
            batch_size=batch_size,
            name="ajibawa-2023/Code-13B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "code-33b":
        return Code(
            batch_size=batch_size,
            name="ajibawa-2023/Code-33B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "phind-code-llama-34b-v2":
        return VLlmDecoder(
            batch_size=batch_size,
            name="Phind/Phind-CodeLlama-34B-v2",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "python-code-33b":
        return Code(
            batch_size=batch_size,
            name="ajibawa-2023/Python-Code-33B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "python-code-13b":
        return Code(
            batch_size=batch_size,
            name="ajibawa-2023/Python-Code-13B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "mistral-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="mistralai/Mistral-7B-v0.1",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "dolphin-2.6":
        return ChatML(
            batch_size=batch_size,
            name="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
            temperature=temperature,
            max_new_tokens=512 + 256,
        )
    elif name == "mixtral-8x7b-instruct":
        return Mixtral(
            batch_size=batch_size,
            name="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=temperature,
        )
    elif name == "solar-10.7b-instruct":
        return Solar(
            batch_size=batch_size,
            name="upstage/SOLAR-10.7B-Instruct-v1.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "mistral-hermes-codepro-7b":
        return ChatML(
            batch_size=batch_size,
            name="beowolx/MistralHermes-CodePro-7B-v1",
            temperature=temperature,
            max_new_tokens=512 + 256,
        )
    elif name == "phi-2":
        return VLlmDecoder(
            batch_size=batch_size,
            name="microsoft/phi-2",
            temperature=temperature,
            dtype="float16",
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "openchat":
        return OpenChat(
            batch_size=batch_size,
            name="openchat/openchat-3.5-0106",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "speechless-codellama-34b":
        return Alpaca(
            batch_size=batch_size,
            name="uukuguy/speechless-codellama-34b-v2.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "speechless-mistral-7b":
        return Alpaca(
            batch_size=batch_size,
            name="uukuguy/speechless-code-mistral-7b-v1.0",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "speechless-coder-ds-6.7b":
        return Speechless(
            batch_size=batch_size,
            name="uukuguy/speechless-coder-ds-6.7b",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "speechless-coding-7b-16k-tora":
        return Speechless(
            batch_size=batch_size,
            name="uukuguy/speechless-coding-7b-16k-tora",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "code-millenials-34b":
        return Alpaca(
            batch_size=batch_size,
            name="budecosystem/code-millenials-34b",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif name == "xdan-l1-chat":
        return Alpaca(
            batch_size=batch_size,
            name="xDAN-AI/xDAN-L1-Chat-dpo-qlora-v1",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "stable-code-3b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="stabilityai/stable-code-3b",
            temperature=temperature,
            trust_remote_code=True,
            dataset=dataset,
        )
    elif name == "xwincoder-34b":
        return XwinCoder(
            batch_size=batch_size,
            name="Xwin-LM/XwinCoder-34B",
            temperature=temperature,
            dataset=dataset,
        )
    elif name == "zyte-1b":
        return Zyte(
            batch_size=batch_size,
            name="aihub-app/zyte-1B",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "white-rabbit-neo-33b-v1":
        return WhiteRabbitNeo(
            batch_size=batch_size,
            name="whiterabbitneo/WhiteRabbitNeo-33B-v-1",
            temperature=temperature,
            direct_completion=False,
            dtype="float16",
        )
    elif "codegemma" in name:
        pattern = re.compile(r"codegemma-(\d+)b")
        matches = pattern.findall(name)
        nb = int(matches[0])
        return CodeGemma(
            batch_size=batch_size,
            name=f"TechxGenus/CodeGemma-{nb}b",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "opencodeinterpreter-ds-6.7b":
        return OpenCodeInterpreterDecoder(
            batch_size=batch_size,
            name="m-a-p/OpenCodeInterpreter-DS-6.7B",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "opencodeinterpreter-ds-33b":
        return OpenCodeInterpreterDecoder(
            batch_size=batch_size,
            name="m-a-p/OpenCodeInterpreter-DS-33B",
            temperature=temperature,
            direct_completion=False,
        )
    elif name == "mistral-large-latest":
        return MistralChatDecoder(
            batch_size=batch_size,
            name="mistral-large-latest",
            temperature=temperature,
            direct_completion=False,
        )

    raise ValueError(f"Invalid model name: {name}")
