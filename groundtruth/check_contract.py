import os
from typing import Dict, Tuple, List
import openai
import re
import json
import wget


MBPP_URL = "https://github.com/google-research/google-research/raw/master/mbpp/sanitized-mbpp.json"

GT_DIR = os.path.dirname(__file__)

MODEL = 'gpt-3.5-turbo'

CONTRACTED_MBPP_PATH = os.path.join(GT_DIR, 'contracted-mbpp.json')

ORIGIN_MBPP_PATH = os.path.join(GT_DIR, 'sanitized-mbpp.json')

SYSTEM_MESSAGE = {'role': 'system', 'content': 'You are a helpful assistant. Please help me to write contracts for those problem'}

EXAMPLE_NUM = 5

def get_indentation(file) -> int:
    with open(file, "r") as file:
        lines = [line for line in file.readlines() if line.strip()]
        for line in lines:
            if len(line - line.lstrip()) > 0:
                return len(line) - len(line.lstrip())
    return 4

def parse_contracts(file) -> str:
    with open(file, 'r') as file:
        content = file.read()

    contract_pattern = re.compile(r'^.*\$_CONTRACT_\$\s*$', re.MULTILINE)
    contracts = [contract.strip('\n\t ') for contract in contract_pattern.findall(content)]

    return contracts

def get_mbpp():
    if not os.path.exists(ORIGIN_MBPP_PATH):
        print("Downloading original MBPP dataset...")
        wget.download(MBPP_URL, ORIGIN_MBPP_PATH)

    with open(ORIGIN_MBPP_PATH, "r") as f:
        mbpp = json.load(f)

    return {str(task["task_id"]): task for task in mbpp}

def dump_contracted_mbpp():
    mbpp = get_mbpp()
    tasks = []
    for tid, task in mbpp.items():
        contracts = parse_contracts(os.path.join(GT_DIR, f'mbpp/{tid.zfill(3)}.py'))
        task['contract_list'] = contracts
        tasks.append(task)

    with open(CONTRACTED_MBPP_PATH, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_contracted_mbpp():
    if not os.path.exists(CONTRACTED_MBPP_PATH):
        print(f"Dumping contracted MBPP dataset to {CONTRACTED_MBPP_PATH}...")
        dump_contracted_mbpp()
    else:
        print(f"Contracted MBPP dataset already exists at {CONTRACTED_MBPP_PATH}.")
        dump_contracted_mbpp()

    with open(CONTRACTED_MBPP_PATH, 'r') as f:
        mbpp = json.load(f)
        return mbpp
    
def construct_message(examples, task):
    messages = [SYSTEM_MESSAGE]
    for example in examples:
        user_content = f"problem description: \n{example['prompt']}\ncode: \n{example['code']}\n"
        messages.append({'role': 'system', 
                         'name': 'example_user', 
                         'content': user_content})
        assistant_content = '\n'.join(example['contract_list'])
        messages.append({'role': 'system',
                         'name': 'example_assistant',
                         'content': assistant_content})
    content = f"problem description: {task['prompt']}\ncode: {task['code']}\n"
    messages.append({'role': 'user', 'content': content})
    return messages

def request_model(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    return response

if __name__ == '__main__':
    openai.api_key = os.environ.get('OPENAI_API_KEY', 'dummy')
    mbpp = load_contracted_mbpp()

    examples, tasks = mbpp[:EXAMPLE_NUM], mbpp[EXAMPLE_NUM:]

    for task in tasks:
        message = construct_message(examples, task)
        response = request_model(message)
        contracts = response['choices'][0]['message']['content'].split('\n')
        # TODO: check handwritten contracts with the gpt generated ones
