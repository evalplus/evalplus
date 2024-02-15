#! /bin/zsh

set -eux

export BS=100
export NS=100
export MODEL=deepseek-coder-6.7b-instruct

python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model $MODEL --prompt-method basic
python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model $MODEL --prompt-method instruct
python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset mbpp --model $MODEL --prompt-method CoT
python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model $MODEL --prompt-method basic
python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model $MODEL --prompt-method CoT
python codegen/generate.py --resume --bs $BS --n_sample $NS --temperature 0.2 --root /scratch/evalplus --dataset humaneval --model $MODEL --prompt-method instruct
