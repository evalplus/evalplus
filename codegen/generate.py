import argparse
import os
from os import PathLike

from model import DecoderBase, make_model
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def construct_contract_prompt(prompt: str, contract_type: str, contract: str) -> str:
    if contract_type == "none":
        return prompt
    elif contract_type == "docstring":
        # embed within the docstring
        sep = ""
        if '"""' in prompt:
            sep = '"""'
        elif "'''" in prompt:
            sep = "'''"
        assert sep != ""
        l = prompt.split(sep)
        contract = "\n".join([x.split("#")[0] for x in contract.splitlines()])
        l[1] = (
            l[1] + contract + "\n" + " " * (len(contract) - len(contract.lstrip()) - 1)
        )
        return sep.join(l)
    elif contract_type == "code":
        # at the beginning of the function
        contract = "\n".join([x.split("#")[0] for x in contract.splitlines()])
        return prompt + contract


def batch(iterable, n=4):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def code_generate(args, workdir: PathLike, model: DecoderBase, id_range=None):
    with Progress(
        TextColumn(
            f"{args.dataset} •" + "[progress.percentage]{task.percentage:>3.0f}%"
        ),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        if args.dataset == "humaneval":
            from evalplus.data import get_human_eval_plus

            dataset = get_human_eval_plus()
        elif args.dataset == "mbpp":
            from evalplus.data import get_mbpp_plus

            dataset = get_mbpp_plus()

        batchs = list(batch(list(dataset.items()), 6))
        for items in p.track(batchs):
            # if id_range is not None:
            #     id_num = int(task_id.split("/")[1])
            #     low, high = id_range
            #     if id_num < low or id_num >= high:
            #         p.console.print(f"Skipping {task_id} as it is not in {id_range}")
            #         continue

            to_process = []
            for task_id, task in items:
                p_name = task_id.replace("/", "_")
                os.makedirs(os.path.join(workdir, p_name), exist_ok=True)
                log = f"Codegen: {p_name} @ {model}"
                n_existing = 0
                if args.resume:
                    # count existing .py files
                    n_existing = len(
                        [
                            f
                            for f in os.listdir(os.path.join(workdir, p_name))
                            if f.endswith(".py")
                        ]
                    )
                    if n_existing > 0:
                        log += f" (resuming from {n_existing})"
                p.console.print(log)
                if n_existing > 0:
                    continue
                to_process.append((p_name, task))

            if not to_process:
                continue

            prompts = [item[1]["prompt"] for item in to_process]
            prompts = [p.rstrip("\n") for p in prompts]
            if args.prompt_method == "zero-shot-CoT" and "instruct" not in args.model:
                hint = "# Let's think step by step to implement an efficient and scalable version:"
                if args.dataset == "humaneval":
                    prompts = [f"{p}\n    {hint}" for p in prompts]
                else:  # mbpp
                    prompts = [f"{p}\n{hint}" for p in prompts]

            outputs = model.codegen(
                prompts,
                do_sample=not args.greedy,
                num_samples=1,
            )
            print(outputs)

            assert outputs, "No outputs from model!"
            for impl, item in zip(outputs, to_process):
                p_name = item[0]
                task = item[1]
                try:
                    with open(
                        os.path.join(workdir, p_name, f"0.py"),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        if model.conversational:
                            f.write(impl)
                        else:
                            f.write(task["prompt"] + impl)
                except UnicodeEncodeError:
                    continue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str)
    parser.add_argument("--bs", default=1, type=int)
    parser.add_argument("--temperature", default=0.0, type=float)
    parser.add_argument(
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )
    parser.add_argument("--root", type=str, required=True)
    parser.add_argument("--n_samples", default=1, type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--contract-type",
        default="none",
        type=str,
        choices=["none", "code", "docstring"],
    )
    parser.add_argument("--greedy", action="store_true")
    # id_range is list
    parser.add_argument("--id-range", default=None, nargs="+", type=int)
    parser.add_argument(
        "--prompt-method", choices=["zero-shot-CoT"], required=False, default=None
    )
    args = parser.parse_args()

    if args.greedy and (args.temperature != 0 or args.bs != 1 or args.n_samples != 1):
        args.temperature = 0
        args.bs = 1
        args.n_samples = 1
        print("Greedy decoding ON (--greedy): setting bs=1, n_samples=1, temperature=0")

    if args.id_range is not None:
        assert len(args.id_range) == 2, "id_range must be a list of length 2"
        assert args.id_range[0] < args.id_range[1], "id_range must be increasing"
        args.id_range = tuple(args.id_range)

    # Make project dir
    os.makedirs(args.root, exist_ok=True)
    # Make dataset dir
    os.makedirs(os.path.join(args.root, args.dataset), exist_ok=True)
    # Make dir for codes generated by each model
    args.model = args.model.lower()
    model = make_model(
        name=args.model,
        batch_size=args.bs,
        temperature=args.temperature,
        prompt_method=args.prompt_method,
    )
    workdir = os.path.join(
        args.root,
        args.dataset,
        args.model
        + f"_temp_{args.temperature}"
        + ("" if args.contract_type == "none" else f"-contract-{args.contract_type}")
        + ("" if args.prompt_method is None else f"-{args.prompt_method}"),
    )
    os.makedirs(workdir, exist_ok=True)

    with open(os.path.join(workdir, "args.txt"), "w") as f:
        f.write(str(args))

    code_generate(args, workdir=workdir, model=model, id_range=args.id_range)


if __name__ == "__main__":
    main()
