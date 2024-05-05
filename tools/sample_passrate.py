import json
from pathlib import Path

from evalplus.eval import estimate_pass_at_k
from evalplus.evaluate import PASS


def get_pass_rate(results: list[dict], ks: list[int], plus: bool) -> dict:
    key = "base_status" if not plus else "plus_status"
    n_samples = len(results)
    n_passed = sum([r[key] == PASS for r in results])
    data = {f"pass{k}": estimate_pass_at_k(n_samples, [n_passed], k).item() for k in ks}
    return data


def main(
    result_path: str,
    output_path: str,
    model: str,
    hyperparams: str,
    ks: list[int] = [1],
    plus: bool = True,
):
    raw_data: dict = json.loads(Path(result_path).read_text())
    eval_result: dict = raw_data["eval"]
    benchmark_id = list(eval_result.keys())[0].split("/")[0] + ("+" if plus else "")
    with Path(output_path).open("w") as f:
        for example_id, example_result in eval_result.items():
            pass_rate = get_pass_rate(example_result, ks, plus)
            data = dict(
                benchmark_id=benchmark_id,
                model=model,
                example_id=example_id,
                hyperparams=hyperparams,
                **pass_rate,
            )
            f.write(json.dumps(data) + "\n")
        f.flush()


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
