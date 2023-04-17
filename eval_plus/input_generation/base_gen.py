class InputGen(object):
    def __init__(self, inputs):
        self.seed_pool = inputs
        self.new_inputs = []
        self.seed_hash = set([hash(str(x)) for x in self.seed_pool])

    def generate(self, num: int):
        raise NotImplementedError
