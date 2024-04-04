# Test-suite Reduction

## Preperation Work

As test-suite reduction relies on the results of evaluation, make sure that you've run the evaluation script and an `eval_results.json` has been generated for each model under test.

Use the following command to install necessary dependencies:

```bash
# in $EVALPLUS_ROOT
pip install -r tools/tsr/requirements.txt
```

## Usage

```bash
python3 run.py \
  --dataset DATASET \
  --sample_eval_dir SAMPLE_DIR \
  --model MODEL \
  [--report_dir REPORT_DIR]

# Example
python3 run.py --dataset humaneval --sample_eval_dir $HOME/HumanEval --model ALL
```

Parameter descriptions:
* `--dataset`: currently, `humaneval` and `mbpp` are supported.
* `--sample_eval_dir` is the directory containing all the LLM evaluation results. We require the directory be structured as
    ```bash
    SAMPLE_EVAL_DIR
    ├── LLM_1
    │   ├── ...
    │   └── eval_results.json
    ├── LLM_2
    │   ├── ...
    ├── ...
    ```
* `--report_dir` is the directory where we store intermediate files, pass@k results, and reduced dataset. If not specified, `REPORT_DIR=./tsr_info` by default.
* If `MODEL` is a specific LLM name, the cross-validation results will be generated in `REPORT_DIR`; if `MODEL == ALL`, a reduced dataset will be generated in `REPORT_DIR`.

## Known Issues

If you find the program stuck at the mutant generation step, try removing the line
```python
assert len(completion_id) == len(problems), "Missing problems in samples"
```
in `evalplus/evaluate.py`.
