model_name=mistral2_instruct

python myEvaluate/evaluate.py --model_name=$model_name --custom=True --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=False
python myEvaluate/evaluate.py --model_name=$model_name --custom=False --evaluate=True