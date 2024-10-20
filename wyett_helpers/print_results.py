import json

with open("inferenced_output/mbpp/mistralai--Mistral-7B-Instruct-v0.3_vllm_temp_0.0-sanitized_eval_results.json", "r") as f:
    strr = f.read()
    
ram = json.loads(str(strr))
print(json.dumps(ram["eval"], indent=4)[:2000])