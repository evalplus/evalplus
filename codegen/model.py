import json
import os
from abc import ABC, abstractmethod
from typing import List
from warnings import warn

# Communism
os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/JawTitan/huggingface/")

import openai
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)
from vllm import LLM, SamplingParams

from evalplus.gen.util.api_request import make_auto_request

EOS = ["<|endoftext|>", "<|endofmask|>", "</s>"]


# Adopted from https://github.com/huggingface/transformers/pull/14897
class EndOfFunctionCriteria(StoppingCriteria):
    def __init__(self, start_length, eos, tokenizer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_length = start_length
        self.eos = eos
        self.tokenizer = tokenizer
        self.end_length = {}

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if all generated sequences contain any of the end-of-function strings."""
        decoded_generations = self.tokenizer.batch_decode(
            input_ids[:, self.start_length :]
        )
        done = []
        for index, decoded_generation in enumerate(decoded_generations):
            finished = any(
                [stop_string in decoded_generation for stop_string in self.eos]
            )
            if (
                finished and index not in self.end_length
            ):  # ensures first time we see it
                for stop_string in self.eos:
                    if stop_string in decoded_generation:
                        self.end_length[index] = len(
                            input_ids[
                                index,  # get length of actual generation
                                self.start_length : -len(
                                    self.tokenizer.encode(
                                        stop_string,
                                        add_special_tokens=False,
                                        return_tensors="pt",
                                    )[0]
                                ),
                            ]
                        )
            done.append(finished)
        return all(done)


class DecoderBase(ABC):
    def __init__(
        self,
        name: str,
        batch_size: int = 1,
        temperature: float = 0.8,
        max_new_tokens: int = 512,
        conversational: bool = False,
        max_conversational_new_tokens: int = 1024,
    ) -> None:
        print("Initializing a decoder model: {} ...".format(name))
        self.name = name
        self.batch_size = batch_size
        self.temperature = temperature
        self.eos = EOS
        self.skip_special_tokens = False
        self.max_new_tokens = (
            max_conversational_new_tokens if conversational else max_new_tokens
        )
        self.conversational = conversational

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

        kwargs = {"tensor_parallel_size": int(os.getenv("VLLM_N_GPUS", "1"))}
        if "CodeLlama" in name:
            kwargs["dtype"] = "bfloat16"
        elif "code-millenials" in name:
            kwargs["dtype"] = "float16"
        elif "uukuguy/speechless-code-mistral-7b-v1.0" == name:
            kwargs["dtype"] = "float16"
        elif "uukuguy/speechless-codellama-34b-v2.0" == name:
            kwargs["dtype"] = "float16"
        elif "CodeBooga" in name:
            kwargs["dtype"] = "float16"
        elif "WizardCoder" in name:
            kwargs["dtype"] = "float16"
        elif "deepseek" in name:
            kwargs["dtype"] = "bfloat16"
        elif "mixtral" in name.lower():
            kwargs["dtype"] = "bfloat16"
        elif "solar" in name:
            kwargs["dtype"] = "float16"
        elif "mistral" in name.lower():
            kwargs["dtype"] = "bfloat16"
        elif "phi" in name.lower():
            kwargs["dtype"] = "float16"
            kwargs["trust_remote_code"] = True
        elif "openchat" in name.lower():
            kwargs["dtype"] = "bfloat16"

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
        kwargs["conversational"] = True
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


class CodeLlamaInstruct(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["conversational"] = True
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
        kwargs["conversational"] = True
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
        kwargs["conversational"] = True
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
        kwargs["conversational"] = True
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


class HFTorchDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        kwargs = {
            "trust_remote_code": name
            in {
                "bigcode/santacoder",
                "Salesforce/codegen2-1B",
                "Salesforce/codegen2-3_7B",
                "Salesforce/codegen2-7B",
                "Salesforce/codegen2-16B",
                "deepseek-ai/deepseek-coder-6.7b-base",
                "deepseek-ai/deepseek-coder-33b-base",
                "stabilityai/stable-code-3b",
            }
        }

        if "codegen-" in name:  # use fp16 for codegen models
            kwargs["torch_dtype"] = torch.float16
        if "codegen2-" in name:  # avoid warning of trust remote code
            kwargs["revision"] = "main"
            if "16b" in name.lower():
                kwargs["device_map"] = "auto"
        if "starcoder" in name:
            kwargs["torch_dtype"] = torch.bfloat16
        if "CodeLlama" in name:
            if "34b" in name.lower():
                kwargs["device_map"] = "auto"
            kwargs["torch_dtype"] = torch.bfloat16
            self.skip_special_tokens = True
        if "CodeBooga" in name:
            kwargs["torch_dtype"] = torch.float16
            kwargs["device_map"] = "auto"
            self.skip_special_tokens = True
        if "Mistral-7B-codealpaca-lora" == name:
            kwargs["torch_dtype"] = torch.float16
            self.skip_special_tokens = True
        elif "Mistral" in name or "zephyr-7b-beta" in name:
            kwargs["torch_dtype"] = torch.bfloat16
        if "deepseek" in name:
            kwargs["torch_dtype"] = torch.bfloat16
            self.skip_special_tokens = True
        if "/phi" in name:
            kwargs["torch_dtype"] = torch.float16
            kwargs["trust_remote_code"] = True
            self.skip_special_tokens = True

        print(f"{kwargs = }")

        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(name, **kwargs)
        if name in {"StabilityAI/stablelm-base-alpha-7b"}:
            print("Switching to float16 ...")
            self.model = self.model.half()
            self.skip_special_tokens = True
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
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        kwargs = {}
        if do_sample:
            kwargs["top_p"] = 0.95
            kwargs["temperature"] = self.temperature

        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            output_scores=True,
            return_dict_in_generate=True,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.eos_token_id,
            **kwargs,
        )  # remove warning
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    # could be multiple eos in outputs, better pick minimum one
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


class DeepSeekInstruct(VLlmDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        kwargs["conversational"] = True
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
        assert batch_size <= 20, "Use larger batch size could blow up the memory!"

        # construct prompt
        fmt = "json_object" if self.name == "gpt-4-1106-preview" else "text"
        if fmt == "json_object":
            message = r'Please complete the following code snippet by generating JSON like {"code": ""}'
        else:
            message = r"Please generate code to complete the following problem:"

        message += f"\n```python\n{prompt.strip()}\n```"

        ret = make_auto_request(
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
        input_tokens = self.tokenizer.encode(input, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            num_return_sequences=min(self.batch_size, num_samples),
            output_scores=True,
            return_dict_in_generate=True,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


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
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        input = prompt + self.infill_ph + self.extra_end
        input_tokens = self.tokenizer.encode(input, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


class SantaCoder(HFTorchDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.prefix_token = "<fim-prefix>"
        self.suffix_token = "<fim-suffix>\n<fim-middle>"
        self.extra_eos = ["<|endofmask|>"]
        self.eos = self.eos + self.extra_eos

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        input = self.prefix_token + prompt + self.suffix_token
        input_tokens = self.tokenizer.encode(input, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            num_return_sequences=min(self.batch_size, num_samples),
            output_scores=True,
            return_dict_in_generate=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs,
            skip_special_tokens=self.skip_special_tokens,
            truncate_before_pattern=[r"\n\n^#", "^'''", "\n\n\n"],
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


class StarCoderInfill(HFTorchDecoder):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.prefix_token = "<fim_prefix>"
        self.suffix_token = "<fim_suffix><fim_middle>"

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        input = self.prefix_token + prompt + self.suffix_token
        input_tokens = self.tokenizer.encode(input, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )

        kwargs = {}
        if do_sample:
            kwargs["top_p"] = 0.95
            kwargs["temperature"] = max(self.temperature, 1e-2)

        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            num_return_sequences=min(self.batch_size, num_samples),
            output_scores=True,
            return_dict_in_generate=True,
            repetition_penalty=1.0,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


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
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        prompt = prompt.replace("    ", "\t")
        input_tokens = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        max_new_tokens = self.max_new_tokens

        while max_new_tokens > 0:
            try:
                raw_outputs = self.model.generate(
                    **input_tokens,
                    decoder_input_ids=input_tokens["input_ids"],
                    max_new_tokens=max_new_tokens,
                    stopping_criteria=scores,
                    do_sample=do_sample,
                    top_p=0.95,
                    top_k=None,
                    temperature=self.temperature,
                    output_scores=True,
                    return_dict_in_generate=True,
                    num_return_sequences=min(self.batch_size, num_samples),
                    pad_token_id=self.tokenizer.eos_token_id,
                    decoder_start_token_id=self.tokenizer.pad_token_id,
                )  # remove warning
            except RuntimeError as e:  # catch torch OOM
                if "CUDA out of memory" in str(e):
                    old_max_new_tokens = max_new_tokens
                    max_new_tokens = int(max_new_tokens * 0.8)
                    print(
                        f"OOM, reducing max_new_tokens from {old_max_new_tokens} to {max_new_tokens}"
                    )
                    continue
                else:
                    raise e

            break
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    # could be multiple eos in outputs, better pick minimum one
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index].replace("\t", "    "))
        return outputs


def make_model(name: str, batch_size: int = 1, temperature: float = 0.8):
    if name == "codegen-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-2B-mono",
            temperature=temperature,
        )
    elif name == "codegen-6b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-6B-mono",
            temperature=temperature,
        )
    elif name == "codegen-16b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-16B-mono",
            temperature=temperature,
        )
    elif name == "codegen2-1b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-1B",
            temperature=temperature,
        )
    elif name == "codegen2-3b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-3_7B",
            temperature=temperature,
        )
    elif name == "codegen2-7b":
        return Codegen2Decoder(
            batch_size=batch_size,
            name="Salesforce/codegen2-7B",
            temperature=temperature,
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
        )
    elif name == "polycoder":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="NinedayWang/PolyCoder-2.7B",
            temperature=temperature,
        )
    elif name == "santacoder":
        return SantaCoder(
            batch_size=batch_size, name="bigcode/santacoder", temperature=temperature
        )
    elif name == "incoder-1b":
        return IncoderDecoder(
            batch_size=batch_size, name="facebook/incoder-1B", temperature=temperature
        )
    elif name == "incoder-6b":
        return IncoderDecoder(
            batch_size=batch_size, name="facebook/incoder-6B", temperature=temperature
        )
    elif name == "stablelm-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="StabilityAI/stablelm-base-alpha-7b",
            temperature=temperature,
        )
    elif name.startswith("gpt-3.5-") or name.startswith("gpt-4-"):
        return OpenAIChatDecoder(
            batch_size=batch_size,
            name=name,
            temperature=temperature,
            conversational=True,
        )
    elif name == "gptneo-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="EleutherAI/gpt-neo-2.7B",
            temperature=temperature,
        )
    elif name == "gpt-j":
        return HFTorchDecoder(
            batch_size=batch_size, name="EleutherAI/gpt-j-6B", temperature=temperature
        )
    elif name.startswith("starcoder"):
        return StarCoderInfill(
            batch_size=batch_size, name=f"bigcode/{name}", temperature=temperature
        )
    elif name == "codet5p-2b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-2b",
            temperature=temperature,
        )
    elif name == "codet5p-6b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-6b",
            temperature=temperature,
        )
    elif name == "codet5p-16b":
        return CodeT5P(
            batch_size=batch_size,
            name="Salesforce/codet5p-16b",
            temperature=temperature,
        )
    elif name.startswith("code-llama-"):
        if name.endswith("instruct"):
            nb = name.split("-")[2]
            assert nb.endswith("b")
            return CodeLlamaInstruct(
                batch_size=batch_size,
                name=f"codellama/CodeLlama-{nb}-Instruct-hf",
                temperature=temperature,
            )

        assert name.endswith("b")
        nb = name.split("-")[-1]
        return VLlmDecoder(
            batch_size=batch_size,
            name=f"codellama/CodeLlama-{nb}-Python-hf",
            temperature=temperature,
        )
    elif name.startswith("deepseek-coder"):
        import re

        # format deepseek-coder-{nb}b*
        pattern = re.compile(r"deepseek-coder-(\d+\.?\d*)b(.*)")
        matches = pattern.findall(name)[0]
        nb = float(matches[0])
        if nb.is_integer():
            nb = int(nb)

        if "instruct" in name:
            return DeepSeekInstruct(
                batch_size=batch_size,
                name=f"deepseek-ai/deepseek-coder-{nb}b-instruct",
                temperature=temperature,
                conversational=True,
            )
        else:
            return VLlmDecoder(
                batch_size=batch_size,
                name=f"deepseek-ai/deepseek-coder-{nb}b-base",
                temperature=temperature,
            )
    elif name == "wizardcoder-34b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-Python-34B-V1.0",
            temperature=temperature,
            conversational=True,
        )
    elif name == "wizardcoder-15b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-15B-V1.0",
            temperature=temperature,
            conversational=True,
        )
    elif name == "wizardcoder-7b":
        return Alpaca(
            batch_size=batch_size,
            name="WizardLM/WizardCoder-Python-7B-V1.0",
            temperature=temperature,
            conversational=True,
        )
    elif name == "mistral-7b-codealpaca":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Nondzu/Mistral-7B-codealpaca-lora",
            temperature=temperature,
        )
    elif name == "zephyr-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="HuggingFaceH4/zephyr-7b-beta",
            temperature=temperature,
        )
    elif name == "codebooga-34b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="oobabooga/CodeBooga-34B-v0.1",
            temperature=temperature,
        )
    elif name == "phind-code-llama-34b-v2":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Phind/Phind-CodeLlama-34B-v2",
            temperature=temperature,
        )
    elif name == "mistral-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="mistralai/Mistral-7B-v0.1",
            temperature=temperature,
        )
    elif name == "dolphin-2.6":
        return ChatML(
            batch_size=batch_size,
            name="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
            temperature=temperature,
            max_new_tokens=512 + 256,
        )
    elif name == "solar-10.7b-instruct":
        return Solar(
            batch_size=batch_size,
            name="upstage/SOLAR-10.7B-Instruct-v1.0",
            temperature=temperature,
            conversational=True,
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
        )
    elif name == "openchat":
        return OpenChat(
            batch_size=batch_size,
            name="openchat/openchat-3.5-0106",
            temperature=temperature,
            conversational=True,
        )
    elif name == "speechless-codellama-34b":
        return Alpaca(
            batch_size=batch_size,
            name="uukuguy/speechless-codellama-34b-v2.0",
            temperature=temperature,
            conversational=True,
        )
    elif name == "speechless-mistral-7b":
        return Alpaca(
            batch_size=batch_size,
            name="uukuguy/speechless-code-mistral-7b-v1.0",
            temperature=temperature,
            conversational=True,
        )
    elif name == "code-millenials-34b":
        return Alpaca(
            batch_size=batch_size,
            name="budecosystem/code-millenials-34b",
            temperature=temperature,
            conversational=True,
        )
    elif name == "xdan-l1-chat":
        return Alpaca(
            batch_size=batch_size,
            name="xDAN-AI/xDAN-L1-Chat-dpo-qlora-v1",
            temperature=temperature,
            conversational=True,
        )
    elif name == "stable-code-3b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="stabilityai/stable-code-3b",
            temperature=temperature,
        )
    elif name == "zyte-1b":
        return Zyte(
            batch_size=batch_size,
            name="aihub-app/zyte-1B",
            temperature=temperature,
            conversational=True,
        )

    raise ValueError(f"Invalid model name: {name}")
