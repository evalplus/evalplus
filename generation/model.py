import os
from typing import List

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


class Decoder(object):
    def __init__(self, batch_size: int = 1, pretrained: str = "gpt2", weight=None):
        print("Initializing a decoder model: {} ...".format(pretrained))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(
            pretrained, torch_dtype=torch.float16
        )
        if weight == "float16":
            print("Switching to float16 ...")
            self.model = self.model.half()
        elif (
            weight == "bfloat16"
        ):  # neo 2.7b can be loaded using only 8 gb with bfloat16
            print("Switching to bfloat16 ...")
            self.model = self.model.to(torch.bfloat16)
        self.model = self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained)
        self.batch_size = batch_size

    # Assumption is that all inputs should probably fit under maximum context. but can add a checking function
    # just in case. TODO: think about

    def generate(
        self, prompt: str, do_sample: bool = True, num_samples: int = 10000
    ) -> List[str]:
        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").repeat(
            min(self.batch_size, num_samples), 1
        )
        input_tokens = input_tokens.to(self.device)
        sc = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eof_strings=EOF_STRINGS,
                    tokenizer=self.tokenizer,
                )
            ]
        )

        with torch.no_grad():
            raw_o = self.model.generate(
                input_tokens,
                max_new_tokens=512,
                stopping_criteria=sc,
                do_sample=do_sample,
                top_p=0.95,
                temperature=0.8,
                output_scores=True,
                return_dict_in_generate=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )  # remove warning
            gen_sequences = raw_o.sequences[:, len(input_tokens[0]) :]
            t_outputs = self.tokenizer.batch_decode(
                gen_sequences, skip_special_tokens=False
            )
            outputs = []
            # removes eof tokens.
            for output in t_outputs:
                min_index = float("inf")
                for eof_string in EOF_STRINGS:
                    if eof_string in output:
                        min_index = min(output.index(eof_string), min_index)
                outputs.append(prompt + output[:min_index])
        return outputs


# TODO: infilling models (e.g., incoder, codet5, etc), if we want to do it, might not be entirely neccessary.
