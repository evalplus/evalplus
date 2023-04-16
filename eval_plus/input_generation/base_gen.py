class InputGen(object):
    def __init__(self, inputs):
        self.seed_pool = inputs
        pass

    def generate(self, num: int):
        raise NotImplementedError
