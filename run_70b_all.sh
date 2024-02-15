#! /bin/zsh

set -eux

export BS=20

python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model code-llama-70b-instruct --prompt-method basic
python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model code-llama-70b-instruct --prompt-method instruct
python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model code-llama-70b-instruct --prompt-method CoT
python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model code-llama-70b-instruct --prompt-method basic
python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model code-llama-70b-instruct --prompt-method CoT
python codegen/generate.py --resume --bs $BS --n_sample 40 --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model code-llama-70b-instruct --prompt-method instruct
