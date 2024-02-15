#! /bin/bash
export PYTHONPATH=$PWD
export CUDA_VISIBLE_DEVICES="6"
export VLLM_N_GPUS=1
set -eux


python codegen/generate.py --resume --root /scratch/evalplus --dataset mbpp \
			   --bs 100 --n_sample 100 --temperature 0.2 \
			   --model code-llama-13b-instruct --prompt-method instruct
python codegen/generate.py --resume --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-13b-instruct --prompt-method instruct

python codegen/generate.py --resume --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-7b-instruct --prompt-method instruct
python codegen/generate.py --resume --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-7b-instruct --prompt-method instruct


python codegen/generate.py --resume --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-6.7b-instruct --prompt-method instruct
python codegen/generate.py --resume --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-6.7b-instruct --prompt-method instruct
