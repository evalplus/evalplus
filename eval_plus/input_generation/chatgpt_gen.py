import ast
import pathlib
import random
from typing import Dict, List

import openai

from eval_plus.input_generation.base_gen import InputGen
from eval_plus.input_generation.util.api_request import (
    create_chatgpt_config,
    request_chatgpt_engine,
)


class ChatGPTGen(InputGen):
    def __init__(self, inputs: List, gd_code: str):
        super().__init__(inputs)
        self.gd_code = gd_code
        self.prompt_message = "Please generate more inputs to test the function."
        key_file = pathlib.Path(__file__).parent / "api_key.txt"
        openai.api_key = open(key_file, "r").read().strip()

    def seed_selection(self) -> List:
        # get 5 for now.
        return random.sample(self.seed_pool, k=min(len(self.seed_pool), 5))

    @staticmethod
    def _parse_ret(ret: Dict) -> List:
        rets = []
        output = ret["choices"][0]["message"]["content"]
        if "```" in output:
            for x in output.split("```")[1].splitlines():
                if x.strip() == "":
                    continue
                try:
                    # remove comments
                    input = ast.literal_eval(f"[{x.split('#')[0].strip()}]")
                except:  # something wrong.
                    continue
                print("Input : {}".format(input))
                rets.append(input)
        return rets

    def chatgpt_generate(self, selected_inputs: List) -> List:
        # append the groundtruth function
        # actually it can be any function (maybe we can generate inputs for each llm generated code individually)
        message = f"Here is a function that we want to test:\n```\n{self.gd_code}\n```"
        str_inputs = "\n".join(
            [", ".join([str(i) for i in x]) for x in selected_inputs]
        )
        message += f"\nThese are some example inputs used to test the function:\n```\n{str_inputs}\n```"
        message += f"\n{self.prompt_message}"
        config = create_chatgpt_config(message, 256)
        ret = request_chatgpt_engine(config)
        return self._parse_ret(ret)

    def generate(self, num: int):
        while len(self.new_inputs) < num:
            seeds = self.seed_selection()
            new_inputs = self.chatgpt_generate(seeds)
            for new_input in new_inputs:
                if hash(str(new_input)) not in self.seed_hash:
                    self.seed_pool.append(new_input)
                    self.seed_hash.add(hash(str(new_input)))
                    self.new_inputs.append(new_input)
        return self.new_inputs
