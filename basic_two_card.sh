export PYTHONPATH=$PWD
export VLLM_N_GPUS=2
set -eux

python codegen/generate.py --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-34b-instruct --prompt-method basic
python codegen/generate.py --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-34b-instruct --prompt-method basic

python codegen/generate.py --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-33b-instruct --prompt-method basic
python codegen/generate.py --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-33b-instruct --prompt-method basic
