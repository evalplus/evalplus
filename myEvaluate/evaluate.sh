model_name=llama_3_instruct_8b_apo_full

python myEvaluate/evaluate.py --model_name=$model_name --custom=True --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=True