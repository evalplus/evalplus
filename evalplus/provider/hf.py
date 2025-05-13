from typing import List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from evalplus.provider.base import DecoderBase
from evalplus.provider.utility import (
    extra_eos_for_direct_completion,
    make_raw_chat_prompt,
)


class HuggingFaceDecoder(DecoderBase):
    def __init__(
        self,
        name: str,
        dataset: str,
        force_base_prompt: bool = False,
        attn_implementation: str = "eager",
        device_map: str = None,
        gguf_file: str = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        kwargs = {
            "device_map": device_map,
            "trust_remote_code": self.trust_remote_code,
            "torch_dtype": getattr(torch, self.dtype),
            "attn_implementation": attn_implementation,  # "eager", "flash_attention_2", "sdpa"
            "gguf_file": gguf_file
        }

        self.skip_special_tokens = True

        print(f"{kwargs = }")

        self.force_base_prompt = force_base_prompt

        # gguf format embeds tokenizer and is not compatible with hf tokenizer `use_fast` param
        tokenizer_kwargs = {}
        if gguf_file is not None:
            tokenizer_kwargs["gguf_file"] = gguf_file
        self.tokenizer = AutoTokenizer.from_pretrained(name, **tokenizer_kwargs)
        if self.is_direct_completion():  # no chat template
            self.eos += extra_eos_for_direct_completion(dataset)
        else:  # with chat template
            self.eos += ["\n```\n"]

        print(f"{self.eos = }")
        self.model = AutoModelForCausalLM.from_pretrained(name, **kwargs)
        self.model = self.model.to(self.device)

    def is_direct_completion(self) -> bool:
        return self.force_base_prompt or self.tokenizer.chat_template is None

    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if self.temperature == 0:
            assert not do_sample
            assert num_samples == 1

        prompt = (
            prompt
            if self.is_direct_completion()
            else make_raw_chat_prompt(
                prompt, self.instruction_prefix, self.response_prefix, self.tokenizer
            )
        )
        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").to(
            self.device
        )
        kwargs = {}
        if do_sample:
            kwargs["top_p"] = 0.95
            kwargs["temperature"] = self.temperature

        outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            do_sample=do_sample,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
            stop_strings=self.eos,
            tokenizer=self.tokenizer,
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
