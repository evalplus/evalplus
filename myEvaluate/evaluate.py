from codegen.generate import main as create_inference
from evalplus.sanitize import script as sanitize
from evalplus.evaluate import main as evaluate_model
from fire import Fire
# tuple in the form of (original model path, original model name, custom model path, custom model name)
MODELS = {
    "llama_3_instruct_8b": (
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "custom_finetuned_models/llama3_instruct_dpo",
    ),
    "llama_3_base_8b": (
        "meta-llama/Meta-Llama-3-8B",
        "custom_finetuned_models/llama3_base_dpo",
    ),
    "deepseek_coder_6.7b_instruct": (
        "meta-llama/Meta-Llama-3-8B",
        "custom_finetuned_models/llama3_base_dpo",
    ),
    "mistral2_instruct": (
        "mistralai/Mistral-7B-Instruct-v0.2",
        "custom_finetuned_models/mistral2_instruct_dpo",
    ),
    "mistral3_base": (
        "mistralai/Mistral-7B-v0.3",
        "custom_finetuned_models/mistral3_base_dpo",
    ),
}


def evaluate(model_name: str, custom: bool, evaluate:bool):
    original_model_path, custom_model_path = MODELS[model_name]
    if custom:
        model_path = custom_model_path
    else:
        model_path = original_model_path
    model_path_2 = model_path.replace("/", "--")
    
    for dataset in ["mbpp", "humaneval"]:
        if not evaluate:
            create_inference(
                model=model_path,
                greedy=True,
                root=f"inferenced_output",
                jsonl_fmt=True,
                dataset=dataset,
                backend="vllm"
            )
            sanitize(samples=f"inferenced_output/{dataset}/{model_path_2}_vllm_temp_0.0.jsonl")
        else:
            print(f"-----------{dataset}--------------")
            print("---------------base-----------------")
            ram = model_path.replace("/", "--")
            evaluate_model(dataset=dataset, samples=f"inferenced_output/{dataset}/{ram}_vllm_temp_0.0-sanitized.jsonl")
            print("---------------fine tuned-----------------")
            ram = custom_model_path.replace("/", "--")
            evaluate_model(dataset=dataset, samples=f"inferenced_output/{dataset}/{ram}_vllm_temp_0.0-sanitized.jsonl")

        
if __name__ == "__main__":
    Fire(evaluate)