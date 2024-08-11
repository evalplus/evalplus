# ------------------------- Default Models ----------------------------------
# inference
python codegen/generate.py --model "meta-llama/Meta-Llama-3-8B-Instruct" --greedy --root "inferenced_output/llama3" --jsonl_fmt --dataset mbpp --backend vllm
python codegen/generate.py --model "meta-llama/Meta-Llama-3-8B-Instruct" --greedy --root "inferenced_output/llama3" --jsonl_fmt --dataset humaneval --backend vllm

python codegen/generate.py --model "deepseek-ai/deepseek-coder-6.7b-instruct" --greedy --root "inferenced_output/ds_6.7b" --jsonl_fmt --dataset mbpp --backend vllm
python codegen/generate.py --model "deepseek-ai/deepseek-coder-6.7b-instruct" --greedy --root "inferenced_output/ds_6.7b" --jsonl_fmt --dataset humaneval --backend vllm

# sanitize
python evalplus/sanitize.py --samples "inferenced_output/llama3/mbpp/meta-llama--Meta-Llama-3-8B-Instruct_vllm_temp_0.0.jsonl"
python evalplus/sanitize.py --samples "/home/wyett/evalplus/inferenced_output/llama3/humaneval/meta-llama--Meta-Llama-3-8B-Instruct_vllm_temp_0.0.jsonl"

# evaluate
python evalplus/evaluate.py --dataset mbpp --samples "/home/wyett/evalplus/inferenced_output/llama3/mbpp/meta-llama--Meta-Llama-3-8B-Instruct_vllm_temp_0.0-sanitized.jsonl"
python evalplus/evaluate.py --dataset humaneval --samples "/home/wyett/evalplus/inferenced_output/llama3/humaneval/meta-llama--Meta-Llama-3-8B-Instruct_vllm_temp_0.0-sanitized.jsonl"

# ------------------------- Finetuned Models ----------------------------------
python codegen/generate.py --model "custom_finetuned_models/llama3_instruct_dpo" --greedy --root "inferenced_output/llama3_finetuned" --jsonl_fmt --dataset mbpp --backend vllm
python evalplus/sanitize.py --samples "/home/wyett/evalplus/inferenced_output/llama3_finetuned/mbpp/custom_finetuned_models--llama3_instruct_dpo_vllm_temp_0.0.jsonl"
python evalplus/evaluate.py --dataset mbpp --samples "/home/wyett/evalplus/inferenced_output/llama3_finetuned/mbpp/custom_finetuned_models--llama3_instruct_dpo_vllm_temp_0.0-sanitized.jsonl"

python codegen/generate.py --model "custom_finetuned_models/llama3_instruct_dpo" --greedy --root "inferenced_output/llama3_finetuned" --jsonl_fmt --dataset humaneval --backend vllm
python evalplus/sanitize.py --samples "/home/wyett/evalplus/inferenced_output/llama3_finetuned/humaneval/custom_finetuned_models--llama3_instruct_dpo_vllm_temp_0.0.jsonl"
python evalplus/evaluate.py --dataset humaneval --samples "inferenced_output/llama3_finetuned/humaneval/custom_finetuned_models--llama3_instruct_dpo_vllm_temp_0.0-sanitized.jsonl"



python codegen/generate.py --model "meta-llama/Meta-Llama-3-8B-Instruct" --greedy --root "inferenced_output/tmp" --jsonl_fmt --dataset mbpp --backend vllm
python codegen/generate.py --model "meta-llama/Meta-Llama-3-8B-Instruct" --greedy --root "inferenced_output/tmp" --jsonl_fmt --dataset humaneval --backend vllm
