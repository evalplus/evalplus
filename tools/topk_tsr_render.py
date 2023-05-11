import json
import os

models = [
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "vicuna-7b",
    "vicuna-13b",
    "stablelm-7b",
    "incoder-1b",
    "incoder-6b",
    "polycoder",
    "chatgpt",
    "santacoder",
    "gptneo-2b",
    "gpt-4",
    "gpt-j",
]

pass_at_k_base = {
    "codegen-2b": 20.7,
    "codegen-6b": 25.6,
    "codegen-16b": 26.8,
    "vicuna-7b": 10.4,
    "vicuna-13b": 15.2,
    "stablelm-7b": 2.4,
    "incoder-1b": 10.4,
    "incoder-6b": 12.2,
    "polycoder": 5.5,
    "chatgpt": 63.4,
    "santacoder": 12.8,
    "gptneo-2b": 6.7,
    "gpt-4": 76.2,
    "gpt-j": 10.4,
}

LLM_HOME_PATH = "/JawTitan/yuyao-data/humaneval"

pass_at_k_before, pass_at_k_after = [], []
for model in models:
    with open(os.path.join(LLM_HOME_PATH, f"{model}.json"), "r") as f:
        info_dict = json.load(f)
    pass_at_k_before.append(f'{info_dict["pass@1_before"] * 100:.1f}')
    pass_at_k_after.append(f'{info_dict["pass@1_after"] * 100:.1f}')
    print(
        model,
        pass_at_k_before[-1],
        pass_at_k_after[-1],
        f"#test: {info_dict['ntests']}",
        f"runtime: {info_dict['runtime_after']}",
    )
