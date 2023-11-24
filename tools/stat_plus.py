import argparse

import numpy as np

from evalplus.data import get_human_eval_plus, get_mbpp_plus

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="humaneval", choices=["mbpp", "humaneval"])
    parser.add_argument("--mini", action="store_true")
    args = parser.parse_args()

    print(f"Reporting stats for {args.dataset} dataset [ mini = {args.mini} ]")
    if args.dataset == "humaneval":
        data = get_human_eval_plus(mini=args.mini)
    elif args.dataset == "mbpp":
        data = get_mbpp_plus(mini=args.mini)

    sizes = np.array(
        [[len(inp["base_input"]), len(inp["plus_input"])] for inp in data.values()]
    )
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
