import json
import multiprocessing
import os

from evalplus._experimental.type_mut_for_eff import TypedMutEffGen
from evalplus.data import HUMANEVAL_PLUS_INPUTS_PATH, get_human_eval_plus

HUMANEVAL_PLUS_BIG_INPUTS_PATH = "/home/yuyao/eval-plus/HumanEvalPlusBigInputs"


def main():
    problems = get_human_eval_plus()
    for p in problems:
        print(f"{p['task_id']}...")
        filename = p["task_id"].replace("/", "_")
        big_input_path = os.path.join(
            HUMANEVAL_PLUS_BIG_INPUTS_PATH, f"{filename}.json"
        )

        if os.path.exists(big_input_path):
            continue
        inputs = p["base_input"]
        signature = p["entry_point"]
        contract_code = p["prompt"] + p["contract"] + p["canonical_solution"]

        def input_generation(inputs, signature, contract_code):
            try:
                gen = TypedMutEffGen(inputs, signature, contract_code)
                new_inputs = gen.generate()
                results.append(new_inputs)
            except:
                with open("fail.txt", "a") as f:
                    f.write(f"{signature} failed")
                results.append("fail")

        manager = multiprocessing.Manager()
        results = manager.list()
        proc = multiprocessing.Process(
            target=input_generation, args=(inputs, signature, contract_code)
        )
        proc.start()
        proc.join(timeout=300)
        if proc.is_alive():
            proc.terminate()
            proc.kill()
            continue
        if len(results) == 0 or type(results[0]) == str:
            continue
        new_inputs = results[0]

        new_input_dict = dict()
        new_input_dict["task_id"] = p["task_id"]
        new_input_dict["inputs"] = []
        new_input_dict["sd"] = []
        for item in new_inputs:
            new_input_dict["inputs"].append(item.inputs)
            new_input_dict["sd"].append(item.fluctuate_ratio)
        with open(
            os.path.join(HUMANEVAL_PLUS_BIG_INPUTS_PATH, f"{filename}.json"), "w"
        ) as f:
            json.dump(new_input_dict, f)


if __name__ == "__main__":
    main()
