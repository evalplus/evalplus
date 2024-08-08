from codegen.generate import main as create_inference
from evalplus.sanitize import script as sanitize
# tuple in the form of (original model path, original model name, custom model path, custom model name)
MODELS = {
    "llama_3_instruct_8b": (
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "llama_3_instruct_8b",
        "custom_finetuned_models/llama3_instruct_dpo",
        "llama3_finetuned",
    ),
    "llama_3_base_8b": (
        "meta-llama/Meta-Llama-3-8B",
        "llama_3_base_8b",
        "custom_finetuned_models/llama3_instruct_dpo",
        "llama3_base_finetuned",
    ),
    "deepseek_coder_6.7b_instruct": (
        "meta-llama/Meta-Llama-3-8B",
        "llama_3_base_8b",
        "custom_finetuned_models/llama3_base_dpo",
        "llama3_base_finetuned",
    ),
}
python evalplus/sanitize.py --samples "inferenced_output/llama3/mbpp/meta-llama--Meta-Llama-3-8B-Instruct_vllm_temp_0.0.jsonl"

def evaluate(model_name: str):
    original_model_path, original_model_name, custom_model_path, custom_model_name = MODELS[model_name]
    for dataset in ["mbpp", "humaneval"]:
        create_inference(
            model=original_model_path,
            greedy=True,
            root=f"inferenced_output/{original_model_name}",
            jsonl_fmt=True,
            database=dataset,
            backend="vllm"
        )
        create_inference(
            model=custom_model_path,
            greedy=True,
            root=f"inferenced_output/{custom_model_name}",
            jsonl_fmt=True,
            database=dataset,
            backend="vllm"
        )
        sanitize(samples=f"inferenced_output/{original_model_name}/{dataset}/{original_model_path}_vllm_temp_0.0.jsonl")