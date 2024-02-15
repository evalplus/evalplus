#! /bin/bash
export PYTHONPATH=$PWD
export CUDA_VISIBLE_DEVICES="4,5"
export VLLM_N_GPUS=2
set -eux

python codegen/generate.py --resume --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-34b-instruct --prompt-method instruct

python codegen/generate.py --resume --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-34b-instruct --prompt-method instruct

python codegen/generate.py --resume --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-33b-instruct --prompt-method instruct

python codegen/generate.py --resume --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-33b-instruct --prompt-method instruct
