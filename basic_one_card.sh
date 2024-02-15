#! /bin/bash
export PYTHONPATH=$PWD
set -eux

python codegen/generate.py --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-6.7b-instruct --prompt-method basic
python codegen/generate.py --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model deepseek-coder-6.7b-instruct --prompt-method basic

python codegen/generate.py --root /scratch/evalplus --dataset mbpp \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-7b-instruct --prompt-method basic
python codegen/generate.py --root /scratch/evalplus --dataset humaneval \
                           --bs 100 --n_sample 100 --temperature 0.2 \
                           --model code-llama-7b-instruct --prompt-method basic
