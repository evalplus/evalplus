from typing import List

import torch
from transformers import AutoTokenizer

try:
    from gptqmodel import GPTQModel
except ModuleNotFoundError as exception:
    raise type(exception)(
        "Tried to load gptqmodel, but gptqmodel is not installed ",
        "please install gptqmodel via `pip install gptqmodel --no-build-isolation`",
    )

from evalplus.provider.base import DecoderBase
from evalplus.provider.utility import (
    extra_eos_for_direct_completion,
    make_raw_chat_prompt,
)


class GPTQModelDecoder(DecoderBase):
    def __init__(
        self,
        name: str,
        dataset: str,
        gptqmodel_backend: str = 'auto',
        force_base_prompt: bool = False,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)

        if hasattr(torch, "mps") and hasattr(torch.mps, "is_available") and torch.mps.is_available():
            device = torch.device("mps")
        elif hasattr(torch, "xpu") and hasattr(torch.xpu, "is_available") and torch.xpu.is_available():
            device = torch.device("xpu")
        elif hasattr(torch, "cuda") and hasattr(torch.cuda, "is_available") and torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

        self.device = device

        kwargs = {
            "model_id_or_path": name,
            "trust_remote_code": self.trust_remote_code,
            "backend": gptqmodel_backend,
            "device": device
        }
        self.skip_special_tokens = True
        self.force_base_prompt = force_base_prompt
        self.tokenizer = AutoTokenizer.from_pretrained(name, trust_remote_code=self.trust_remote_code)
        if self.is_direct_completion():  # no chat template
            self.eos += extra_eos_for_direct_completion(dataset)
        else:  # with chat template
            self.eos += ["\n```\n"]
        self.model = GPTQModel.load(**kwargs)
        self.model = self.model.to(self.device)

    def is_direct_completion(self) -> bool:
        return self.force_base_prompt or self.tokenizer.chat_template is None

    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        prompt = (
            prompt
            if self.is_direct_completion()
            else make_raw_chat_prompt(
                prompt, self.instruction_prefix, self.response_prefix, self.tokenizer
            )
        )
        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(input_ids=input_tokens,
                                      pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
                                      max_new_tokens=self.max_new_tokens)

        gen_strs = self.tokenizer.batch_decode(
            outputs[:, input_tokens.size(-1):],
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
