import json
import os

LLM_HOME_PATH = "/JawTitan/yuyao-data/humaneval"

models = [
    "gpt-4",
    "chatgpt",
    "starcoder",
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "codegen2-1b",
    "codegen2-3b",
    "codegen2-7b",
    "codegen2-16b",
    "vicuna-7b",
    "vicuna-13b",
    "santacoder",
    "incoder-1b",
    "incoder-6b",
    "gpt-j",
    "gptneo-2b",
    "polycoder",
    "stablelm-7b",
]

info_dict = {"s1": {}, "s2": {}}


def collect_s1(model, stage, type, full_dict):
    with open(os.path.join(LLM_HOME_PATH, f"{model}_{stage}_{type}.json"), "r") as f:
        cov_dict = json.load(f)
    pass_at_k_up = round((cov_dict["pass@1"] - full_dict["pass@1"]) * 100, 1)
    test_down = full_dict["ntests"] - cov_dict["ntests"]
    return round(pass_at_k_up, 1), round(test_down, 1)


def s1_print(type):
    print(
        f' & \diff{{{info_dict["s1"][type][0]}}}{{{info_dict["s1"][type][1]}}}', end=""
    )


def s2_print(type):
    print(f' & $\grow{{{info_dict["s2"][type][0]}}}$', end="")


def full_print(stage):
    print(
        f' & \exact{{{info_dict[stage]["full"][0]}}}{{{info_dict[stage]["full"][1]}}}',
        end="",
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str)
    args = parser.parse_args()

    # stage 1
    for i, model in enumerate(models):
        args.model = model
        info_dict = {"s1": {}, "s2": {}}
        with open(os.path.join(LLM_HOME_PATH, f"{args.model}_s1_full.json"), "r") as f:
            full_dict = json.load(f)
        info_dict["s1"]["coverage"] = collect_s1(
            args.model, "s1", "coverage", full_dict
        )
        info_dict["s1"]["mutation"] = collect_s1(
            args.model, "s1", "mutation", full_dict
        )
        info_dict["s1"]["sample"] = collect_s1(args.model, "s1", "sample", full_dict)
        info_dict["s1"]["full"] = (
            round(full_dict["pass@1"] * 100, 1),
            round(full_dict["ntests"], 1),
        )

        # stage 2
        with open(os.path.join(LLM_HOME_PATH, f"{args.model}_s2_full.json"), "r") as f:
            full_dict = json.load(f)
        info_dict["s2"]["coverage"] = collect_s1(
            args.model, "s2", "coverage", full_dict
        )
        info_dict["s2"]["mutation"] = collect_s1(
            args.model, "s2", "mutation", full_dict
        )
        info_dict["s2"]["sample"] = collect_s1(args.model, "s2", "sample", full_dict)
        info_dict["s2"]["full"] = (
            round(full_dict["pass@1"] * 100, 1),
            round(full_dict["ntests"], 1),
        )

        s1_print("coverage")
        s1_print("mutation")
        s1_print("sample")
        full_print("s1")
        print("")
        s2_print("coverage")
        s2_print("mutation")
        s2_print("sample")
        full_print("s2")
        if (
            i < len(models) - 1
            and models[i + 1][0] != models[i][0]
            or model == "gpt-j"
            or model == "codegen-16b"
        ):
            print("\n")
        else:
            print("")
