import copy


class BaseGen(object):
    def __init__(self, inputs, signature, contract_code):
        self.contract_code = contract_code
        self.signature = signature
        self.seed_pool = copy.deepcopy(inputs)
        self.new_inputs = []
        self.seed_hash = set([hash(str(x)) for x in self.seed_pool])

    def generate(self, num: int):
        raise NotImplementedError
