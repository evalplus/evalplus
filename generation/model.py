import os
from typing import List
from abc import ABC, abstractmethod

import openai
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

# os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/ColossalTitan/huggingface/")  # I don't like colossaltitan


EOF_STRINGS = ["\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif"]


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

    @abstractmethod
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        pass


class OpenAIDecoder(DecoderBase):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        openai.api_key = os.environ.get("OPENAI_API_KEY", "dummy")
        openai.api_base = os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:5000/v1")

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        assert do_sample, "Currently we let OpenAI API only support sampling"
        batch_size = min(self.batch_size, num_samples)
        assert batch_size <= 10, "Use larger batch size could blow up the memory!"

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

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class HFTorchDecoder(DecoderBase):
    def __init__(
        self,
        name: str,
        batch_size: int = 1,
        temperature: float = 0.8,
        weight=None,
    ):
        super().__init__(name=name, batch_size=batch_size, temperature=temperature)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(
            name, torch_dtype=torch.float16
        )
        if weight == "float16":
            print("Switching to float16 ...")
            self.model = self.model.half()
        elif weight == "bfloat16":
            # neo 2.7b can be loaded using only 8 gb with bfloat16
            print("Switching to bfloat16 ...")
            self.model = self.model.to(torch.bfloat16)
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
                    eof_strings=EOF_STRINGS,
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
        gen_strs = self.tokenizer.batch_decode(gen_seqs, skip_special_tokens=False)
        outputs = []
        # removes eof tokens.
        for output in gen_strs:
            min_index = None
            for eof_string in EOF_STRINGS:
                if eof_string in output:
                    min_index = output.index(eof_string)
                    break
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


# TODO: infilling models (e.g., incoder, codet5, etc), if we want to do it, might not be entirely neccessary.
