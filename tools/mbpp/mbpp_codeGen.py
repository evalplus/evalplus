import os
import pathlib
import re
import json
import wget
import sys
from typing import Dict, Tuple, List

from chatGPT_engine import ChatGPTEngine


CACHE_DIR = "tmp"
EXAMPLE_PATH = "../../groundtruth/mbpp/" 
GPT_CONTRACT_PATH = "contract.json"
MAX_TOKENS = 512
MBPP_URL = "https://github.com/google-research/google-research/raw/master/mbpp/sanitized-mbpp.json"
MBPP_PLUS_VERSION = "v0.0.0"
PROMPT_PATH = "prompt.txt"


def get_mbpp() -> Dict[str, Dict]:
    """Get MBPP from Google's Github repo."""
    mbpp_path = os.path.join(CACHE_DIR, "sanitized-mbpp.json")
    mbpp = None

    if not os.path.exists(mbpp_path):
        # create CACHE_DIR if not exists
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        # Install MBPP-sanitized from scratch
        print("Downloading original MBPP dataset...")
        wget.download(MBPP_URL, mbpp_path)

    with open(mbpp_path, "r") as f:
        mbpp = json.load(f)

    return {str(task["task_id"]): task for task in mbpp}

class mbppCheck:
    def __init__(self, id: int):
        self.mbpp = get_mbpp()
        self.chatgpt = ChatGPTEngine()
        self.last_tid = id
        self.contract = {}

        with open(EXAMPLE_PATH+"002.py", 'r') as f:
            self.example = f.read()
        
        with open(PROMPT_PATH, 'r') as f:
            self.prompt = f.read()

        if not os.path.exists(GPT_CONTRACT_PATH):
            with open(GPT_CONTRACT_PATH, 'w') as f:
                json.dump({}, f)
    
    def message_gen(self, task: Dict):
        newline = "\n"
        message_codeblock_split = "\n---\n"  # Conventional delimiter when interacting with chatgpt

        incomplete = f'''"""
{task["prompt"]}
"""

{task["code"]}

{newline.join(task["test_imports"])}

{newline.join(task["test_list"])}
'''
        self.message = self.prompt + message_codeblock_split \
         + incomplete + message_codeblock_split# + self.example + message_codeblock_split 
        return

    @staticmethod
    def extract_contract(input: str) -> Tuple:
        contracts = []
        in_comment = False
        for line in input.split('\n'):
            if '"""' in line:
                in_comment = not in_comment
            if not in_comment and '# $_CONTRACT_$' in line:
                contract = line.split('# $_CONTRACT_$')[0].strip()
                contracts.append(contract)
        return tuple(contracts)


    def contract_generate(self):
        for tid, task in self.mbpp.items():
            if int(tid) <= self.last_tid:
                continue

            ground_truth_path = os.path.join(EXAMPLE_PATH, f"{tid.zfill(3)}.py")
            if os.path.exists(ground_truth_path):
                with open(ground_truth_path, 'r') as f:
                    ground_truth = f.read()
            else:
                print(f"File {filename} doesn't exist, skip...")
                continue

            print("-----The contact for code {} is being generated----".format(tid))
            # 1. Get a response from chatgpt
            self.message_gen(task)
            config = self.chatgpt.create_chatgpt_config(self.message, MAX_TOKENS)
            resp = self.chatgpt.request(config)
            raw_ret = self.chatgpt._parse_ret(resp)

            # 2. Extract contracts from response
            try:
                gpt_contract = self.extract_contract(raw_ret)
            except Exception as e:
                print(f"Exception occurred: {e}")
                self.save_contract()
                raise SystemExit(1)

            # 3. Extract contracts from ground_truth
            self.contract[tid.zfill(3)] = gpt_contract
            ground_truth_contract = self.extract_contract(ground_truth)

            if set(gpt_contract) == set(ground_truth_contract):
                print("-----TEST PASS-----")
            else:
                print(raw_ret)
                print("-----TEST FAILED-----")
                print("gpt:")
                print("\n".join(gpt_contract))
                print("ground truth:")
                print("\n".join(ground_truth_contract))
                return


    def save_contract(self):
        with open(GPT_CONTRACT_PATH, 'r') as f:
            gpt_contract_dict = json.load(f)
        self.contract = {**self.contract, **gpt_contract_dict}
        with open(GPT_CONTRACT_PATH, 'w') as f:
            json.dump(self.contract, f)
        print("Record-keeping completed")



if __name__ == '__main__':
    script_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(script_path))

    if len(sys.argv) > 1:
        start_id = int(sys.argv[1])
    checker = mbppCheck(start_id)
    checker.contract_generate()
    checker.save_contract()