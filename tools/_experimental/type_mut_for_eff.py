import copy
import math
import random
import string
from typing import Any, Dict, List, Optional, Set, Tuple

from multipledispatch import dispatch
from rich.progress import track

from evalplus._experimental.evaluate_runtime import (
    MAX_WARMUP_LIMIT,
    RUN_REPEAT,
    execute_for_runtime,
)
from evalplus.gen.mut_gen import MutateGen

MUTATE_BOUND_SIZE = 5
MAX_MULTI_STEP_SIZE = 1000
MAX_SEED_POOL = 10

NoneType = type(None)
MAX_SIZE = 80000
VALUE_MAX = 1000000


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


class TestInput:
    def __init__(self, inputs: List, runtime: float, sd: float):
        self.inputs = inputs
        self.sz = self.typed_size(inputs)
        self.runtime = runtime
        self.sd = sd
        self.rank_sd = self.rank_sz = 1

    def __str__(self):
        return str(self.inputs)

    @property
    def fluctuate_ratio(self) -> float:
        return self.sd / self.runtime * 100

    @property
    def rank(self) -> float:
        return self.rank_sd * (self.rank_sz**0.8) if self.sz <= 2000 else self.rank_sd

    @dispatch(NoneType)
    def typed_size(self, _) -> int:
        return 1

    @dispatch(int)
    def typed_size(self, _) -> int:
        return 1

    @dispatch(float)
    def typed_size(self, _) -> int:
        return 1

    @dispatch(bool)
    def typed_size(self, _) -> int:
        return 1

    @dispatch(str)
    def typed_size(self, s: str) -> int:
        return len(s)

    @dispatch(list)
    def typed_size(self, l: list) -> int:
        return sum(self.typed_size(x) for x in l)

    @dispatch(tuple)
    def typed_size(self, t: tuple) -> int:
        return sum(self.typed_size(x) for x in t)

    @dispatch(set)
    def typed_size(self, s: set) -> int:
        return sum(self.typed_size(x) for x in s)

    @dispatch(dict)
    def typed_size(self, d: dict) -> int:
        return sum(self.typed_size(x) for x in d.items())


class TypedMutEffGen(MutateGen):
    def __init__(self, inputs: List, signature: str, contract_code: str):
        super().__init__(inputs, signature, contract_code)

        self.base_inputs = copy.deepcopy(inputs)
        self.seed_pool: List[TestInput] = []
        self.seed_hash: Set[str] = set()
        for base_input in self.base_inputs:
            avg, sd = self.test_efficiency(base_input)
            assert avg != None and sd != None, "base inputs not correct"
            self.insert_input(TestInput(base_input, avg, sd))
            self.seed_hash.add(hash(str(base_input)))

        self.ingredients = {
            int: set(),
            float: set(),
            str: set(),
        }
        for x in inputs:
            self.fetch_ingredient(x)

    def insert_input(self, new_input: TestInput):
        new_input_hash = hash(str(new_input))
        if new_input_hash in self.seed_hash:
            return
        self.seed_pool.append(new_input)
        self.seed_pool.sort(key=lambda x: x.fluctuate_ratio)
        self.seed_hash.add(new_input_hash)

        if len(self.seed_pool) > MAX_SEED_POOL:
            self.seed_pool.sort(key=lambda x: x.fluctuate_ratio)
            for i in range(len(self.seed_pool)):
                self.seed_pool[i].rank_sd = i + 1
            self.seed_pool.sort(key=lambda x: -x.sz)
            for i in range(len(self.seed_pool)):
                self.seed_pool[i].rank_sz = i + 1
            self.seed_pool.sort(key=lambda x: x.rank)
            seed_deleted = self.seed_pool[-1]
            self.seed_hash.remove(hash(str(seed_deleted)))
            self.seed_pool = self.seed_pool[:-1]

    def test_efficiency(self, new_input: List) -> Tuple[Optional[float]]:
        warmups = []
        new_input_hash = hash(str(new_input))
        for input_list in self.base_inputs:
            if (
                len(warmups) < MAX_WARMUP_LIMIT
                and hash(str(input_list)) != new_input_hash
            ):
                warmups.append(input_list)
        runtime_list = [
            execute_for_runtime(self.contract_code, new_input, warmups, self.signature)
            for _ in range(RUN_REPEAT)
        ]
        if any(type(x) != float for x in runtime_list):
            return None, None
        avg = sum(runtime_list) / RUN_REPEAT
        sd = math.sqrt(sum((t - avg) ** 2 for t in runtime_list) / (RUN_REPEAT - 1))
        return avg, sd

    #########################
    # Type-aware generation #
    #########################
    @dispatch(NoneType)
    def typed_gen(self, _):
        return None

    @dispatch(int)
    def typed_gen(self, _):
        @use_ingredient(0.5)
        def _impl(*_):
            return random.randint(-VALUE_MAX, VALUE_MAX)

        return _impl(self, _)

    @dispatch(float)
    def typed_gen(self, _):
        @use_ingredient(0.5)
        def _impl(*_):
            return random.uniform(-VALUE_MAX, VALUE_MAX)

        return _impl(self, _)

    @dispatch(bool)
    def typed_gen(self, _):
        return random.choice([True, False])

    @dispatch(str)
    def typed_gen(self, _):
        @use_ingredient(0.5)
        def _impl(*_):
            return "".join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(0, 10))
            )

        return _impl(self, _)

    def any_gen(self):
        # weighted choose
        choice = random.choices(
            [
                True,
                1,
                1.1,
                "str",
                [],  # list
                tuple(),  # tuple
                dict(),  # dict
                None,  # None
            ],
            [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05],
        )[0]
        return self.typed_gen(choice)

    @dispatch(list)
    def typed_gen(self, _):
        ret = []
        size = random.randint(0, 10)
        if random.randint(0, 4) == 0:  # heterogeneous
            for _ in range(size):
                ret.append(self.any_gen())
        else:  # homogeneous
            t = random.choice([bool(), int(), float(), str()])
            for _ in range(size):
                ret.append(self.typed_gen(t))
        return ret

    @dispatch(tuple)
    def typed_gen(self, _):
        return tuple(self.typed_gen([]))

    # NOTE: disable set for now as Steven is too weak in Python (/s)
    # @dispatch(set)
    # def typed_gen(self, _):
    #     return set(self.typed_gen([]))

    @dispatch(dict)
    def typed_gen(self, _):
        ret = dict()
        values = self.typed_gen([])
        # NOTE: Assumption: nobody uses dict with heterogeneous keys
        # NOTE: Assumption: nobody uses dict with boolean keys
        key_type = random.choice([int(), float(), str()])
        for v in values:
            ret[self.typed_gen(key_type)] = self.typed_gen(v)
        return ret

    ########################
    # Type-aware mutation  #
    ########################
    # Simple primitives
    @dispatch(int)
    def typed_mutate(self, seed_input: int):
        @use_ingredient(0.1)
        def _impl(_, seed_input: int):
            prob = random.uniform(0, 1)
            if 0 <= prob < 0.2:
                return seed_input * 2
            elif 0.2 <= prob < 0.9:
                return random.randint(-VALUE_MAX, VALUE_MAX)
            else:
                return seed_input + 5

        return _impl(self, seed_input)

    @dispatch(float)
    def typed_mutate(self, seed_input: float):
        @use_ingredient(0.1)
        def _impl(_, seed_input: float):
            prob = random.uniform(0, 1)
            if 0 <= prob < 0.2:
                return seed_input * (2 + random.uniform(-0.5, 0.5))
            elif 0.2 <= prob < 0.9:
                return random.uniform(-VALUE_MAX, VALUE_MAX)
            else:
                return seed_input + 5.0

        return _impl(self, seed_input)

    @dispatch(bool)
    def typed_mutate(self, seed_input: bool):
        return random.choice([True, False])

    @dispatch(NoneType)
    def typed_mutate(self, seed_input: NoneType):
        return None

    # List-like
    @dispatch(list)
    def typed_mutate(self, seed_input: List):
        if len(seed_input) == 0:
            return self.typed_gen([])

        choice = random.randint(1, 3)
        idx = random.randint(0, len(seed_input) - 1)
        if choice == 1 and 0 < len(seed_input) < MAX_SIZE:  # length *= 1.1
            old_length = len(seed_input)
            new_length = math.ceil(old_length * 1.1)
            for _ in range(new_length - old_length):
                seed_input.insert(
                    random.randint(0, len(seed_input) - 1),
                    self.typed_mutate(seed_input[idx]),
                )
        elif choice == 2 and 0 < len(seed_input) < MAX_SIZE:  # repeat, length *= 1.1
            old_length = len(seed_input)
            new_length = math.ceil(old_length * 1.1)
            for _ in range(new_length - old_length):
                seed_input.append(seed_input[idx])
        else:  # inplace element change, large_scale
            for idx in range(len(seed_input)):
                if random.uniform(0, 1) > 0.7:
                    seed_input[idx] = self.typed_mutate(seed_input[idx])
        return seed_input

    @dispatch(tuple)
    def typed_mutate(self, seed_input: Tuple):
        return tuple(self.typed_mutate(list(seed_input)))

    # String
    @dispatch(str)
    def typed_mutate(self, seed_input: str):
        @use_ingredient(0.1)
        def _impl(_, seed_input: str):
            choice = random.randint(0, 2) if seed_input else 0
            if (
                choice <= 1 and self.ingredients[str]
            ):  # insert ingredients, length *= 1.1
                new_length = math.ceil(len(seed_input) * 1.1)
                while len(seed_input) < new_length:
                    idx = random.randint(0, len(seed_input))
                    seed_input = (
                        seed_input[:idx]
                        + random.choice(list(self.ingredients[str]))
                        + seed_input[idx:]
                    )
                return seed_input
            # other choices assume len(seed_input) > 0
            elif choice == 2:  # inplace mutation, large_scale
                ch_list = []
                for i in range(len(seed_input)):
                    if random.uniform(0, 1) > 0.7:
                        ch_list.append(random.choice(string.ascii_letters))
                    else:
                        ch_list.append(seed_input[i])
                return "".join(ch_list)

            # random char
            return self.typed_gen(str())

        return _impl(self, seed_input)

    # Set
    @dispatch(set)
    def typed_mutate(self, seed_input: Set):
        return set(self.typed_mutate(list(seed_input)))

    # Dict
    @dispatch(dict)
    def typed_mutate(self, seed_input: Dict):
        if len(seed_input) == 0:
            return self.typed_gen(dict())

        choice = random.randint(1, 2)
        if choice == 1:  # add a kv
            k = self.typed_mutate(random.choice(list(seed_input.keys())))
            v = self.typed_mutate(random.choice(list(seed_input.values())))
            seed_input[k] = v
        elif choice == 2:  # inplace value change
            k0, v0 = random.choice(list(seed_input.items()))
            seed_input[k0] = self.typed_mutate(v0)
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
        for token in seed_input.strip().split():
            self.ingredients[str].add(token)

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

    # NOTE: disable set for now as Steven is too weak in Python (/s)
    # @dispatch(set)
    # def typed_fetch(self, seed_input: Set):
    #     self._fetch_list_like(seed_input)

    # Dict
    @dispatch(dict)
    def typed_fetch(self, seed_input: Dict):
        self._fetch_list_like(seed_input.keys())
        self._fetch_list_like(seed_input.values())

    # Type-aware concatenation

    @dispatch(int, int)
    def concat(x: int, y: int):
        return x + y

    @dispatch(float, float)
    def concat(x: float, y: float):
        return x + y

    @dispatch(bool, bool)
    def concat(x: bool, y: bool):
        return random.choice([x, y])

    @dispatch(NoneType, NoneType)
    def concat(x: NoneType, y: NoneType):
        return None

    @dispatch(list, list)
    def concat(x: list, y: list):
        choice = random.randint(0, 1)
        return (
            copy.deepcopy(x) + copy.deepcopy(y)
            if choice == 0
            else copy.deepcopy(y) + copy.deepcopy(x)
        )

    @dispatch(str, str)
    def concat(x: str, y: str):
        choice = random.randint(0, 1)
        return x + y if choice == 0 else y + x

    @dispatch(set, set)
    def concat(x: set, y: set):
        return x.union(y)

    @dispatch(dict, dict)
    def concat(x: dict, y: dict):
        return x.update(y)

    def mutate(self, seed: TestInput) -> List[Any]:
        new_input = copy.deepcopy(seed.inputs)

        for _ in range(20):
            prob = random.uniform(0, 1)
            if 0 <= prob < 0.1 and seed.sz <= MAX_SIZE:
                another_seed = random.choice(self.seed_pool).inputs
                new_input = [
                    self.concat(new_input[i], another_seed[i])
                    for i in range(len(new_input))
                ]
            else:
                for i in range(len(new_input)):
                    new_input[i] = self.typed_mutate(new_input[i])

        return new_input

    def generate(self) -> List[TestInput]:
        for _ in track(range(40)):
            seed = self.seed_selection()
            new_input = self.mutate(seed)
            # print(len(new_input[0]))
            avg, sd = self.test_efficiency(new_input)
            if avg != None and sd != None:
                self.insert_input(TestInput(new_input, avg, sd))
        return self.seed_pool


if __name__ == "__main__":
    from evalplus.data import get_human_eval_plus

    problems = get_human_eval_plus()
    for p in problems[43:44]:
        inputs = p["base_input"]
        entry_point = p["entry_point"]
        contract = p["prompt"] + p["contract"] + p["canonical_solution"]
        gen = TypedMutEffGen(inputs, entry_point, contract)
        new_inputs = gen.generate()
        for i, new_input in enumerate(new_inputs):
            print(f"New input {i}: sz: {new_input.sz}")
            if new_input.sz <= 10:
                print(new_input.inputs)
            print(
                f"- Runtime: {new_input.runtime}, Sd: {new_input.sd}, Per: {new_input.fluctuate_ratio}"
            )
