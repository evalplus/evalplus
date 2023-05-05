import os
from abc import ABC, abstractmethod
from typing import List
from warnings import warn

# Communism
os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/ColossalTitan/huggingface/")

import openai

# ==============================================================
# # The vicuna-7b weights are at /ColossalTitan/vicuna/vicuna-7b
# Made by running:
# ```
# python3 -m fastchat.model.apply_delta \
#     --base /ColossalTitan/llama/converted_hf_7B \
#     --target /ColossalTitan/vicuna/vicuna-7b \
#     --delta lmsys/vicuna-7b-delta-v1.1
# ```
# ==============================================================
# The vicuna-13b weights are at /ColossalTitan/vicuna/vicuna-13b
# Made by running:
# ```
# python3 -m fastchat.model.apply_delta \
#     --base /ColossalTitan/llama/converted_hf_13B \
#     --target /ColossalTitan/vicuna/vicuna-13b \
#     --delta lmsys/vicuna-13b-delta-v1.1
# ```
# ==============================================================
# Acknoledgement:
# Modified from https://github.com/lm-sys/FastChat/blob/main/fastchat/serve/huggingface_api.py
import torch
from fastchat.serve.inference import load_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

from evalplus.gen.util.api_request import create_chatgpt_config, request_chatgpt_engine

NON_CODE_EOFS = ["<|endoftext|>", "\n```", "\n</s>", "<|endofmask|>"]
EOF_STRINGS = [
    "\nclass",
    "\ndef",
    "\n#",
    "\n@",
    "\nprint",
    "\nif",
] + NON_CODE_EOFS


# Adopted from https://github.com/huggingface/transformers/pull/14897
class EndOfFunctionCriteria(StoppingCriteria):
    def __init__(self, start_length, eof_strings, tokenizer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_length = start_length
        self.eof_strings = eof_strings
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
                [stop_string in decoded_generation for stop_string in self.eof_strings]
            )
            if (
                finished and index not in self.end_length
            ):  # ensures first time we see it
                for stop_string in self.eof_strings:
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
    ) -> None:
        print("Initializing a decoder model: {} ...".format(name))
        self.name = name
        self.batch_size = batch_size
        self.temperature = temperature
        self.eofs = EOF_STRINGS
        self.skip_special_tokens = False

    @abstractmethod
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        pass

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class OpenAIDecoder(DecoderBase):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        openai.api_key = os.environ.get("OPENAI_API_KEY", "dummy")
        FAUXIPILOT_ADDR = None
        if name == "codegen-16b":
            FAUXIPILOT_ADDR = "http://127.0.0.1:5000/v1"
        elif name == "codegen-6b":
            FAUXIPILOT_ADDR = "http://127.0.0.1:5010/v1"
        openai.api_base = os.environ.get("OPENAI_API_BASE", FAUXIPILOT_ADDR)

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        # assert do_sample, "Currently we let OpenAI API only support sampling"
        batch_size = min(self.batch_size, num_samples)
        assert batch_size <= 20, "Use larger batch size could blow up the memory!"

        ret = openai.Completion.create(
            model="fastertransformer",
            prompt=prompt,
            max_tokens=512,
            temperature=self.temperature,
            n=batch_size,
            stop=EOF_STRINGS,
        )

        # assert the ret are not empty
        assert len(ret["choices"]) > 0, "OpenAI API returns empty results!"

        # process the output and return
        return [x["text"] for x in ret["choices"]]


class HFTorchDecoder(DecoderBase):
    def __init__(self, name: str, batch_size: int = 1, temperature: float = 0.8):
        super().__init__(name=name, batch_size=batch_size, temperature=temperature)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        kwargs = {
            "trust_remote_code": name
            in {
                "bigcode/santacoder",
                "Salesforce/codegen2-1B",
                "Salesforce/codegen2-3_7B",
                "Salesforce/codegen2-7B",
                "Salesforce/codegen2-16B",
            }
        }
        if "codegen-" in name:  # use fp16 for codegen models
            kwargs["torch_dtype"] = torch.float16
        if (
            "codegen2-" in name
        ):  # specify a branch to avoid warning of trust remote code
            kwargs["revision"] = "main"
        self.model = AutoModelForCausalLM.from_pretrained(name, **kwargs)
        if name in {"StabilityAI/stablelm-base-alpha-7b"}:
            self.skip_special_tokens = True
            print("Switching to float16 ...")
            self.model = self.model.half()
        if "codegen2-" in name:  # switch codegen2 to float16
            kwargs["revision"] = "main"
            print("Switching to float16 ...")
            self.model = self.model.half()
        self.model = self.model.to(self.device)

    # Assumption is that all inputs should probably fit under maximum context. but can add a checking function
    # just in case. TODO: think about
    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input_tokens = (
            self.tokenizer.encode(prompt, return_tensors="pt")
            .repeat(min(self.batch_size, num_samples), 1)
            .to(self.device)
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eof_strings=self.eofs,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=512,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )  # remove warning
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eof tokens.
        for output in gen_strs:
            min_index = 10000
            for eof_string in EOF_STRINGS:
                if eof_string in output:
                    # could be multiple eof in outputs, better pick minimum one
                    min_index = min(min_index, output.index(eof_string))
            outputs.append(output[:min_index])
        return outputs


class FsChatDecoder(HFTorchDecoder):
    def __init__(self, name: str, batch_size: int = 1, temperature: float = 0.8):
        DecoderBase.__init__(
            self, name=name, batch_size=batch_size, temperature=temperature
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.tokenizer = load_model(
            f"/ColossalTitan/vicuna/{name}",
            device="cuda",
            num_gpus=1,
            load_8bit=False,
            debug=False,
        )


class ChatGPTDecoder(DecoderBase):
    def __init__(
        self,
        name: str,
        batch_size: int = 1,
        temperature: float = 0.8,
        model_name: str = "gpt-3.5-turbo",
    ) -> None:
        super().__init__(name, batch_size, temperature)
        self.model_name = model_name
        openai.api_key = os.environ.get("OPENAI_API_KEY", "dummy")

    @staticmethod
    def _find_gen_func_sig(prompt):
        func_sig = ""
        for x in prompt.splitlines():
            if x.startswith("def ") and x.endswith(":"):
                # always pick the last one, since there could pre-defined functions.
                func_sig = x
        return func_sig

    @staticmethod
    def _remove_eof(gen):
        min_index = 1000
        for eof_string in EOF_STRINGS:
            if eof_string in gen:
                min_index = min(min_index, gen.index(eof_string))
        return gen[:min_index]

    def _chatgpt_parse(self, ret, prompt):
        outputs = []
        for returns in ret["choices"]:
            raw_o = returns["message"]["content"]
            if "```" in raw_o:
                gen = raw_o.split("```")[1].strip()
                if gen.startswith("python"):
                    gen = gen[len("python") :].strip()
                if gen.startswith(prompt.strip()):
                    suf = gen.split(prompt.strip())[-1]
                    suf = self._remove_eof(suf)
                    gen = prompt.strip() + suf
                elif self._find_gen_func_sig(prompt) in gen:
                    # same function sign is in the prompt
                    sig = self._find_gen_func_sig(prompt)
                    pre, suf = gen.split(sig)[0], gen.split(sig)[-1]
                    suf = self._remove_eof(suf)
                    gen = pre + sig + suf
                else:
                    gen = f"# CANNOT PARSE CODE SNIPPET\n{gen}"
            else:
                # cannot really handle parse just dump to file and maybe process later.
                gen = f"# CANNOT PARSE\n{raw_o}"
            outputs.append(gen)
        return outputs

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        # assert do_sample, "Currently we let OpenAI API only support sampling"
        batch_size = min(self.batch_size, num_samples)
        assert batch_size <= 20, "Use larger batch size could blow up the memory!"

        # construct prompt
        message = (
            f"Please complete the following code snippet.\n```\n{prompt.strip()}\n```"
        )
        config = create_chatgpt_config(
            message=message,
            # max_tokens = 512, # for regular generation
            max_tokens=1024,
            temperature=self.temperature,
            batch_size=batch_size,
            model=self.model_name,
        )
        ret = request_chatgpt_engine(config)
        return self._chatgpt_parse(ret, prompt.strip())


class IncoderDecoder(HFTorchDecoder):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        self.infill_ph = "<|mask:0|>"
        self.extra_end = "<|mask:1|><|mask:0|>"
        self.extra_eof = [
            "<|endofmask|>",
            "<|/ file",
            "</cell>",
            "</text>",
            "</code>",
            "<|",
            "</CODE>",
        ]
        self.eofs = self.eofs + self.extra_eof

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = prompt + self.infill_ph + self.extra_end
        input_tokens = (
            self.tokenizer.encode(input, return_tensors="pt")
            .repeat(min(self.batch_size, num_samples), 1)
            .to(self.device)
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eof_strings=self.eofs,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=512,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eof tokens.
        for output in gen_strs:
            min_index = 10000
            for eof_string in self.eofs:
                if eof_string in output:
                    min_index = min(min_index, output.index(eof_string))
            outputs.append(output[:min_index])
        return outputs


class Codegen2Decoder(HFTorchDecoder):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        self.infill_ph = "<mask_1>"
        # taken from: https://huggingface.co/Salesforce/codegen2-16B
        self.extra_end = "<|endoftext|><sep><mask_1>"
        self.extra_eof = ["<eom>"]
        self.eofs = self.eofs + self.extra_eof

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = prompt + self.infill_ph + self.extra_end
        input_tokens = (
            self.tokenizer.encode(input, return_tensors="pt")
            .repeat(min(self.batch_size, num_samples), 1)
            .to(self.device)
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eof_strings=self.eofs,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=512,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eof tokens.
        for output in gen_strs:
            min_index = 10000
            for eof_string in self.eofs:
                if eof_string in output:
                    min_index = min(min_index, output.index(eof_string))
            outputs.append(output[:min_index])
        return outputs


class SantaDecoder(HFTorchDecoder):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        self.prefix_token = "<fim-prefix>"
        self.suffix_token = "<fim-suffix>\n<fim-middle>"
        self.extra_eof = ["<|endofmask|>"]
        self.eofs = self.eofs + self.extra_eof

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = self.prefix_token + prompt + self.suffix_token
        input_tokens = (
            self.tokenizer.encode(input, return_tensors="pt")
            .repeat(min(self.batch_size, num_samples), 1)
            .to(self.device)
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eof_strings=self.eofs,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=512,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eof tokens.
        for output in gen_strs:
            min_index = 10000
            for eof_string in self.eofs:
                if eof_string in output:
                    min_index = min(min_index, output.index(eof_string))
            outputs.append(output[:min_index])
        return outputs


def make_model(
    name: str,
    batch_size: int = 1,
    temperature: float = 0.8,
):
    if name == "codegen-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-2B-mono",
            temperature=temperature,
        )
    elif name == "codegen-6b":
        warn(
            "Using fauxipilot backend for codegen-6b by default. "
            "If you wish to use huggingface backend go `codegen-6b-hf`"
        )
        return OpenAIDecoder(
            batch_size=batch_size,
            name="codegen-6b",
            temperature=temperature,
        )
    elif name == "codegen-6b-hf":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="Salesforce/codegen-6B-mono",
            temperature=temperature,
        )
    elif name == "codegen-16b":
        return OpenAIDecoder(
            batch_size=batch_size,
            name="codegen-16b",
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
    elif name == "vicuna-7b" or name == "vicuna-13b":
        return FsChatDecoder(
            batch_size=batch_size,
            name=name,
            temperature=temperature,
        )
    elif name == "santacoder":
        return SantaDecoder(
            batch_size=batch_size,
            name="bigcode/santacoder",
            temperature=temperature,
        )
    elif name == "incoder-1b":
        return IncoderDecoder(
            batch_size=batch_size,
            name="facebook/incoder-1B",
            temperature=temperature,
        )
    elif name == "incoder-6b":
        return IncoderDecoder(
            batch_size=batch_size,
            name="facebook/incoder-6B",
            temperature=temperature,
        )
    elif name == "stablelm-7b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="StabilityAI/stablelm-base-alpha-7b",
            temperature=temperature,
        )
    elif name == "chatgpt":
        return ChatGPTDecoder(
            batch_size=batch_size,
            name="ChatGPT",
            temperature=temperature,
            model_name="gpt-3.5-turbo",
        )
    elif name == "gpt-4":
        return ChatGPTDecoder(
            batch_size=batch_size,
            name="GPT4",
            temperature=temperature,
            model_name="gpt-4",
        )
    elif name == "gptneo-2b":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="EleutherAI/gpt-neo-2.7B",
            temperature=temperature,
        )
    elif name == "gpt-j":
        return HFTorchDecoder(
            batch_size=batch_size,
            name="EleutherAI/gpt-j-6B",
            temperature=temperature,
        )

    raise ValueError(
        f"Invalid model name: {name}"
        + R"""
    Supported models:
    - codegen-2b
    - codegen-6b
    - codegen-16b
    # Add more manually in `make_model` function
    """
    )
