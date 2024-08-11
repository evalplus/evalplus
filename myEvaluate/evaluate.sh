model_name=mistral3_base

python myEvaluate/evaluate.py --model_name=$model_name --custom=True --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=True