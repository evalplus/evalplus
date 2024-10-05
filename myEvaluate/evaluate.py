from codegen.generate import main as create_inference
from evalplus.sanitize import script as sanitize
from evalplus.evaluate import main as evaluate_model
from fire import Fire
# tuple in the form of (original model path, original model name, custom model path, custom model name)
MODELS = {
    "llama_3_instruct_8b_dpo_full": (
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "trained_models/llama_3_instruct/full/dpo/1",
    ),
    "llama_3_instruct_8b_apo_full": (
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "trained_models/llama_3_instruct/full/apo_zero/1",
    ),
    "mistral_3_instruct_dpo_full": (
        "mistralai/Mistral-7B-Instruct-v0.3",
        "custom_saved_models/mistral_3_instruct/full/dpo",
    ),
}


def evaluate(model_name: str, custom: bool, evaluate:bool):
    original_model_path, custom_model_path = MODELS[model_name]
    if custom:
        model_path = custom_model_path
    else:
        model_path = original_model_path
    model_path_2 = model_path.replace("/", "--")
    
    for dataset in ["humaneval", "mbpp"]:
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
            print("---------------Pre-finetuned-----------------")
            ram = model_path.replace("/", "--")
            evaluate_model(dataset=dataset, samples=f"inferenced_output/{dataset}/{ram}_vllm_temp_0.0-sanitized.jsonl")
            print("---------------Post-finetuned----------------")
            ram = custom_model_path.replace("/", "--")
            evaluate_model(dataset=dataset, samples=f"inferenced_output/{dataset}/{ram}_vllm_temp_0.0-sanitized.jsonl")

        
if __name__ == "__main__":
    Fire(evaluate)