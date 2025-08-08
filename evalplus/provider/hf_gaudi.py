import copy
import time
from typing import List
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import habana_frameworks.torch.hpu as torch_hpu

from evalplus.provider.base import DecoderBase
from evalplus.provider.utility import (
    extra_eos_for_direct_completion,
    make_raw_chat_prompt,
)

import habana_frameworks.torch.core as htcore
from optimum.habana.transformers.modeling_utils import adapt_transformers_to_gaudi

from optimum.habana.transformers.trainer import _is_peft_model

adapt_transformers_to_gaudi()


def get_torch_compiled_model(model):
    # for gpt_bigcode, mpt, bloom, gpt2 model_type
    if hasattr(model, "transformer"):
        model.transformer = torch.compile(
            model.transformer, backend="hpu_backend", options={"keep_input_mutations": True}
        )
    # for gpt_neox
    elif hasattr(model, "gpt_neox"):
        model.gpt_neox = torch.compile(model.gpt_neox, backend="hpu_backend", options={"keep_input_mutations": True})
    # for llama, mistral, mixtral, qwen2
    elif hasattr(model, "model"):
        model.model = torch.compile(model.model, backend="hpu_backend", options={"keep_input_mutations": True})
    else:
        model = torch.compile(model, backend="hpu_backend", options={"keep_input_mutations": True})
    return model

class HuggingFaceDecoder(DecoderBase):
    def __init__(
        self,
        name: str,
        dataset: str,
        force_base_prompt: bool = False,
        device_map: str = None,
        gguf_file: str = None,
        **kwargs,
    ):
        
        print("Kwargs: {}".format(kwargs))
        super().__init__(name=name, **kwargs)
        #self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("hpu")
        self.dtype =  "bfloat16"
        
        if kwargs.get("torch_compile", False):
            self.torch_compile = True
            self.lazy_mode = False
            self.hpu_graphs = False
        else:
            self.torch_compile = False
            self.lazy_mode = True
            self.hpu_graphs = True

        model_kwargs = {
            "device_map": device_map,
            "trust_remote_code": self.trust_remote_code,
            "torch_dtype": getattr(torch, self.dtype),
            "gguf_file": gguf_file
        }

        self.skip_special_tokens = True

        print(f"{model_kwargs = }")

        self.force_base_prompt = force_base_prompt

        # gguf format embeds tokenizer and is not compatible with hf tokenizer `use_fast` param
        tokenizer_kwargs = {}
        if gguf_file is None:
            tokenizer_kwargs["use_fast"] = False
        else:
            tokenizer_kwargs["gguf_file"] = gguf_file
        self.tokenizer = AutoTokenizer.from_pretrained(name,
                                                       torch_dtype=self.dtype,
                                                        **tokenizer_kwargs)
        if self.is_direct_completion():  # no chat template
            self.eos += extra_eos_for_direct_completion(dataset)
        else:  # with chat template
            self.eos += ["\n```\n"]

        self.model = AutoModelForCausalLM.from_pretrained(name, **model_kwargs)
        self.model = self.model.eval().to(self.device)

        
        if self.torch_compile:
            self.model = get_torch_compiled_model(self.model)
        else:
            from habana_frameworks.torch.hpu import wrap_in_hpu_graph
            self.model = wrap_in_hpu_graph(self.model)

            if _is_peft_model(self.model):
                self.model.base_model = wrap_in_hpu_graph(self.model.base_model)
                if self.model.peft_type == "ADAPTION_PROMPT":
                    self.model.base_model.model = wrap_in_hpu_graph(self.model.base_model.model)

        self.generation_config = copy.deepcopy(self.model.generation_config)
        self.generation_config.use_cache = kwargs.get("use_cache", True)
        self.generation_config.attn_softmax_bf16 = kwargs.get("attn_softmax_bf16", True)
        self.generation_config.reuse_cache = kwargs.get("reuse_cache", True)
        self.generation_config.use_flash_attention = kwargs.get("use_flash_attention", True)
        self.generation_config.flash_attention_recompute = kwargs.get("flash_attention_recompute", True)
        self.generation_config.flash_attention_causal_mask = kwargs.get("flash_attention_causal_mask", True)
        self.generation_config.flash_attention_fast_softmax = kwargs.get("flash_attention_fast_softmax", True)
        self.generation_config.reduce_recompile = kwargs.get("reduce_recompile", False)
        self.generation_config.clear_hpu_graphs_cache = kwargs.get("clear_hpu_graphs_cache", False)

    def is_direct_completion(self) -> bool:
        return self.force_base_prompt or self.tokenizer.chat_template is None
    
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
        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
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
            hpu_graphs=self.hpu_graphs,
            lazy_mode=self.lazy_mode,
            generation_config=self.generation_config,
            **kwargs,
        ).cpu()

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
