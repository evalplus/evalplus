import numpy as np

from eval_plus.utils import get_human_eval_plus, get_human_eval_plus_inputs

if __name__ == "__main__":
    size_base = np.array([len(inp["base_input"]) for inp in get_human_eval_plus()])
    print(f"{size_base.min() = }", f"{size_base.argmin() = }")
    print(f"{size_base.max() = }", f"{size_base.argmax() = }")
    print(f"{np.percentile(size_base, 50) = :.1f}")
    print(f"{size_base.mean() = :.1f}")

    size_plus = np.array([len(inp) for inp in get_human_eval_plus_inputs().values()])
    size_plus += size_base
    print(f"{size_plus.min() = }", f"{size_plus.argmin() = }")
    print(f"{size_plus.max() = }", f"{size_plus.argmax() = }")
    print(f"{np.percentile(size_plus, 50) = :.1f}")
    print(f"{size_plus.mean() = :.1f}")
