from multipledispatch import dispatch

import copy
import random
from typing import List, Any, Tuple, Set, Dict

from eval_plus.evaluation.evaluate import execute
from eval_plus.input_generation.mut_gen import MutateGen

MAX_MULTI_STEP_SIZE = 5


# decorator to use ingredients
class use_ingredient:
    def __init__(self, prob: float):
        assert 0 <= prob <= 0.95
        self.prob = prob

    def __call__(obj, func):
        def wrapper(self, seed_input):
            if random.random() < obj.prob and self.ingredients[type(seed_input)]:
                return random.choice(list(self.ingredients[type(seed_input)]))
            else:
                return func(self, seed_input)

        return wrapper


class TypedMutGen(MutateGen):
    def __init__(self, inputs: List, signature: str, contract_code: str):
        super().__init__(inputs, signature, contract_code)
        self.ingredients = {
            int: set(),
            float: set(),
            str: set(),
        }

    def seed_selection(self):
        # random for now.
        return random.choice(self.seed_pool)

    def mutate(self, seed_input: Any) -> List:
        new_input = copy.deepcopy(seed_input)

        while new_input == seed_input:
            new_input = self.typed_mutate(new_input)

        return new_input

    ########################
    # Type-aware mutation  #
    ########################

    # Simple primitives
    @dispatch(int)
    # @use_ingredient(0.5)
    def typed_mutate(self, seed_input: int):
        return seed_input + random.randint(-1, 1)

    @dispatch(float)
    # @use_ingredient(0.5)
    def typed_mutate(self, seed_input: float):
        return seed_input + random.uniform(-1, 1)

    @dispatch(bool)
    def typed_mutate(self, seed_input: bool):
        return random.choice([True, False])

    # List-like
    def _mutate_list_like(self, seed_input):
        idx = random.randint(0, len(seed_input) - 1)

        choice = random.randint(0, 3)
        if choice == 0 and len(seed_input) > 0:  # remove one element
            seed_input.pop(random.randint(0, len(seed_input) - 1))
        elif choice == 1:  # add one mutated element
            seed_input.append(self.mutate(seed_input[idx]))
        elif choice == 2:  # repeat one element
            seed_input.append(seed_input[idx])
        else:  # inplace element change
            seed_input[idx] = self.mutate(seed_input[idx])
        return seed_input

    @dispatch(str)
    # @use_ingredient(0.5)
    def typed_mutate(self, seed_input: str):
        return "".join(self._mutate_list_like([*seed_input]))

    @dispatch(list)
    def typed_mutate(self, seed_input: List):
        return self._mutate_list_like(seed_input)

    @dispatch(tuple)
    def typed_mutate(self, seed_input: Tuple):
        return tuple(self._mutate_list_like(list(seed_input)))

    # Set
    @dispatch(set)
    def typed_mutate(self, seed_input: Set):
        return set(self._mutate_list_like(list(seed_input)))

    # Dict
    @dispatch(dict)
    def typed_mutate(self, seed_input: Dict):
        choice = random.randint(0, 2)
        if choice == 0 and len(seed_input) > 0:  # remove a kv
            del seed_input[random.choice(list(seed_input.keys()))]
        elif choice == 1:  # add a kv
            k = self.mutate(random.choice(list(seed_input.keys())))
            v = self.mutate(random.choice(list(seed_input.values())))
            seed_input[k] = v
        else:  # inplace value change
            k0, v0 = random.choice(list(seed_input.items()))
            seed_input[k0] = self.mutate(v0)
        return seed_input

    ############################################
    # Fetching ingredients to self.ingredients #
    ############################################
    def fetch_ingredient(self, seed_input):
        self.typed_fetch(seed_input)

    @dispatch(int)
    def typed_fetch(self, seed_input: int):
        self.ingredients[int].add(seed_input)

    @dispatch(float)
    def typed_fetch(self, seed_input: float):
        self.ingredients[float].add(seed_input)

    @dispatch(str)
    def typed_fetch(self, seed_input: str):
        self.ingredients[str].add(seed_input)

    # List-like
    def _fetch_list_like(self, seed_input):
        for x in seed_input:
            if self.typed_fetch.dispatch(type(x)):
                self.fetch_ingredient(x)

    @dispatch(list)
    def typed_fetch(self, seed_input: List):
        self._fetch_list_like(seed_input)

    @dispatch(tuple)
    def typed_fetch(self, seed_input: Tuple):
        self._fetch_list_like(seed_input)

    @dispatch(set)
    def typed_fetch(self, seed_input: Set):
        self._fetch_list_like(seed_input)

    # Dict
    @dispatch(dict)
    def typed_fetch(self, seed_input: Dict):
        self._fetch_list_like(seed_input.keys())
        self._fetch_list_like(seed_input.values())

    def generate(self, num: int):
        while len(self.new_inputs) < num:
            new_input = self.seed_selection()
            # Multi-step instead of single-step
            for _ in range(random.randint(1, MAX_MULTI_STEP_SIZE)):
                new_input = self.mutate(new_input)
            if hash(str(new_input)) not in self.seed_hash:
                o = execute(self.contract_code, new_input, self.signature)
                if o != "timed out" and o != "thrown exception":
                    self.typed_fetch(new_input)
                    self.seed_pool.append(new_input)
                    self.seed_hash.add(hash(str(new_input)))
                    self.new_inputs.append(new_input)
        return self.new_inputs[:num]
