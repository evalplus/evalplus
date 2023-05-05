import numpy as np

from evalplus.data import get_human_eval_plus

if __name__ == "__main__":
    sizes = [
        [len(inp["base_input"]), len(inp["plus_input"])]
        for inp in get_human_eval_plus().values()
    ]
    size_base = sizes[:, 0]
    print(f"{size_base.min() = }", f"{size_base.argmin() = }")
    print(f"{size_base.max() = }", f"{size_base.argmax() = }")
    print(f"{np.percentile(size_base, 50) = :.1f}")
    print(f"{size_base.mean() = :.1f}")

    size_plus = sizes[:, 1]
    size_plus += size_base
    print(f"{size_plus.min() = }", f"{size_plus.argmin() = }")
    print(f"{size_plus.max() = }", f"{size_plus.argmax() = }")
    print(f"{np.percentile(size_plus, 50) = :.1f}")
    print(f"{size_plus.mean() = :.1f}")
