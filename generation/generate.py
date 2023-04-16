import argparse
import os

# TODO: setup our own human_eval package that can provides better separation.
from human_eval.data import read_problems, write_jsonl
from model import Decoder


def code_generate(args, model: Decoder, problems):
    for p_name, problem in problems.items():
        p_name = p_name.replace("/", "_")
        os.makedirs(os.path.join(args.folder, p_name), exist_ok=True)
        print("generating for {} ...".format(p_name))
        for l_samples in range(args.n_samples, 0, -args.bs):
            generations = model.generate(problem["prompt"], num_samples=l_samples)
            for i, code_func in enumerate(generations):
                with open(
                    os.path.join(
                        args.folder,
                        p_name,
                        "{}.py".format(args.n_samples - l_samples + i),
                    ),
                    "w",
                ) as f:
                    f.write(code_func)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=str)
    parser.add_argument("--folder", required=True, type=str)
    parser.add_argument("--model", required=True, type=str)
    parser.add_argument("--bs", required=True, type=int)
    parser.add_argument("--temperature", required=True, type=float)
    parser.add_argument("--n_samples", required=True, type=int)
    args = parser.parse_args()

    if args.dataset not in ["humaneval"]:
        raise NotImplementedError("Unsupported dataset: {}".format(args.dataset))

    os.makedirs(args.folder, exist_ok=True)
    with open(os.path.join(args.folder, "args.txt"), "w") as f:
        f.write(str(args))

    problems = read_problems()
    model = Decoder(batch_size=args.bs, pretrained=args.model)
    code_generate(args, model, problems)


if __name__ == "__main__":
    main()
