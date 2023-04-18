import copy
import random
import string
from typing import List, Any

from eval_plus.evaluation.evaluate import execute
from eval_plus.input_generation.base_gen import BaseGen


class MutateGen(BaseGen):
    def __init__(self, inputs: List, signature: str, contract_code: str):
        super().__init__(inputs, signature, contract_code)

    def seed_selection(self):
        # random for now.
        return random.choice(self.seed_pool)

    def mutate(self, seed_input: Any) -> List:
        new_input = copy.deepcopy(seed_input)

        while hash(str(new_input)) == hash(str(seed_input)):
            strategy = random.randint(0, 7)
            if len(new_input) == 0:
                break
            element = random.randint(0, len(new_input) - 1)
            # increment
            if strategy == 0:
                if type(new_input[element]) in {int, float}:
                    new_input[element] += 1
            # decrement
            elif strategy == 1:
                if type(new_input[element]) in {int, float}:
                    new_input[element] -= 1
            # negative
            elif strategy == 2:
                if type(new_input[element]) in {int, float}:
                    new_input[element] = -new_input[element]
            # string bitflip
            # elif strategy == 3:
            #     if type(new_input[element]) in {str}:
            #         index = random.randint(0, len(new_input[element])-1)
            #         new_input[element][index] = random.choice(string.ascii_letters)
            # string add character
            elif strategy == 4:
                if type(new_input[element]) in {str}:
                    index = random.randint(0, len(new_input[element]))
                    if index == len(new_input[element]):
                        new_input[element] = new_input[element] + random.choice(
                            string.ascii_letters
                        )
                    else:
                        new_input[element] = (
                            new_input[element][:index]
                            + random.choice(string.ascii_letters)
                            + new_input[element][index:]
                        )
            # string remove character.
            elif strategy == 5:
                if type(new_input[element]) in {str}:
                    index = random.randint(0, len(new_input[element]))
                    if index == len(new_input[element]):
                        break
                    else:
                        s = str(
                            new_input[element][: index - 1] + new_input[element][index:]
                        )
                        new_input[element] = s
            # list add element
            elif strategy == 6:
                if type(new_input[element]) in {list}:
                    if len(new_input[element]) == 0:
                        break
                    index = random.randint(0, len(new_input[element]) - 1)
                    if type(new_input[element][index]) in {int, float}:
                        new_input[element].append(
                            type(new_input[element][index])(random.randrange(0, 100))
                        )
                    if type(new_input[element][index]) in {str}:
                        new_input[element].append(
                            "".join(
                                random.choices(
                                    string.ascii_letters, k=random.randint(1, 7)
                                )
                            )
                        )
            # list remove element.
            elif strategy == 7:
                if type(new_input[element]) in {list}:
                    if len(new_input[element]) == 0:
                        break
                    index = random.randint(0, len(new_input[element]) - 1)
                    new_input[element].pop(index)

        return new_input

    def generate(self, num: int):
        while len(self.new_inputs) < num:
            seed = self.seed_selection()
            new_input = self.mutate(seed)
            if hash(str(new_input)) not in self.seed_hash:
                o = execute(self.contract_code, new_input, self.signature)
                if o != "timed out" and o != "thrown exception":
                    self.seed_pool.append(new_input)
                    self.seed_hash.add(hash(str(new_input)))
                    self.new_inputs.append(new_input)
        return self.new_inputs[:num]
