# EvalPlus Commands

* `evalplus.codegen`: Code generation + Code post-processing
* `evalplus.evaluate`: Code generation + Code post-processing + Evaluation
* `evalplus.sanitize`: Code post-processing

## Code Generation

`evalplus.codegen` support following backends:

- `vllm`: Set `--model` as Hugging Face model ID such as `microsoft/Phi-3-mini-128k-instruct`
- `hf`: HuggingFace Transformers; same way to setup `--model`
- `openai`: Configure `OPENAI_API_KEY`; one can configure `--base-url`
- `anthropic`: Configure `ANTHROPIC_API_KEY`
- `google`: Configure `GOOGLE_API_KEY`
- `bedrock`: Configure `BEDROCK_ROLE_ARN`
- `gptqmodel`: Set quantized `--model` as Hugging Face model ID such as `ModelCloud/Qwen2.5-Coder-32B-Instruct-gptqmodel-4bit-vortex-v1`

```shell
evalplus.codegen --model "mistralai/Mistral-7B-Instruct-v0.3" --greedy --root [result_path] --dataset [mbpp|humaneval] --backend [vllm|hf|openai|...]
```

To perform code generation using user-defined tasks and datasets:

```shell
# Override HumanEval datasets
HUMANEVAL_OVERRIDE_PATH="/path/to/HumanEvalPlus.jsonl.gz" evalplus.codegen --model "mistralai/Mistral-7B-Instruct-v0.3" --greedy --root [result_path] --dataset humaneval --backend [vllm|hf|openai|...]
# Override MBPP datasets
MBPP_OVERRIDE_PATH="/path/to/MbppPlus.jsonl.gz" evalplus.codegen --model "mistralai/Mistral-7B-Instruct-v0.3" --greedy --root [result_path] --dataset mbpp --backend [vllm|hf|openai|...]
```

## Customized Code Generation

You can perform your own code generation from scratch by doing something like this:

```python
from evalplus.data import get_[human_eval|mbpp]_plus, write_jsonl

samples = [
    dict(task_id=task_id, solution=GEN_SOLUTION(problem["prompt"]))
    for task_id, problem in get_[human_eval|mbpp]_plus().items()
]
write_jsonl("samples.jsonl", samples)
```

> [!Note]
>
> The main structure of `problem` is as follows:
>
> - `task_id` is the identifier string for the task
> - `entry_point` is name of the function
> - `prompt` is the function signature with docstring
> - `canonical_solution` is the ground-truth implementation (re-implemented to fix bugs in HumanEval)
> - `base_input` is the test inputs in original HumanEval
> - `plus_input` is the test inputs brought by EvalPlus

> [!Note]
>
> **Expected Schema of `samples.jsonl`**
>
> 1. `task_id`: Task ID, which are the keys of `get_[human_eval|mbpp]_plus()`
> 2. `solution` (optional): Self-contained solution (usually including the prompt)
>    - Example: `{"task_id": "HumanEval/?", "solution": "def f():\n    return 1"}`
> 3. `completion` (optional): Function body without prompt
>    - Example: `{"task_id": "HumanEval/?", "completion": "    return 1"}`
>
> Only one of `solution` and `completion` is required. If both are provided, `solution` will be used.
> We also accept solutions in the form of directory, i.e., `--samples ${SAMPLE_DIR}` where `${SAMPLE_DIR}` is organized as: `${SAMPLE_DIR}/${TASK_ID}/{SAMPLE_ID}.py` (`${TASK_ID} = task_id.replace("/", "_")`).

## Code post-processing

> [!Note]
>
> This step is by default performed in `evalplus.codegen`.
> Yet, you might want to use it if you have generated the code using other tools.

LLM-generated text may not be compilable code for including natural language lines or incomplete extra code.
We provide a tool namely `evalplus.sanitize` to clean up the code:

```shell
# 💡 If you are storing codes in jsonl:
evalplus.sanitize --samples samples.jsonl
# Sanitized code will be produced to `samples-sanitized.jsonl`

# 💡 If you are storing codes in directories:
evalplus.sanitize --samples /path/to/vicuna-[??]b_temp_[??]
# Sanitized code will be produced to `/path/to/vicuna-[??]b_temp_[??]-sanitized`
```

<details><summary>🔎 Checking the compilability of post-processed code<i>:: click to expand ::</i></summary>
<div>

To double-check the post-processing results, you can use `evalplus.syncheck` to check the code validity before and after sanitization, which will print erroneous code snippets and why they are wrong:

```shell
# 💡 If you are storing codes in jsonl:
evalplus.syncheck --samples samples.jsonl --dataset [humaneval|mbpp]

# 💡 If you are storing codes in directories:
evalplus.syncheck --samples /path/to/vicuna-[??]b_temp_[??] --dataset [humaneval|mbpp]
```

</div>
</details>



## Code Evaluation

You are strongly recommended to use a sandbox such as [docker](https://docs.docker.com/get-docker/):

```bash
docker run --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval                                     \
           --samples /app/humaneval/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_0.0.jsonl
```

...Or if you want to try it locally regardless of the risks ⚠️:

```bash
evalplus.evaluate --dataset [humaneval|mbpp] --samples samples.jsonl
```

To use a user-defined dataset locally, you can set `HUMANEVAL_OVERRIDE_PATH` or `MBPP_OVERRIDE_PATH`:

```bash
HUMANEVAL_OVERRIDE_PATH="/path/to/HumanEvalPlus.jsonl.gz" evalplus.evaluate --dataset humaneval --samples samples.jsonl
```

> [!Tip]
>
> Program execution can be configured. See [Program Execution in EvalPlus and EvalPerf](./docs/execution.md).

<details><summary>🤔 Evaluate with local GitHub repo? <i>:: click to expand ::</i></summary>
<div>

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python evalplus/evaluate.py --dataset humaneval --samples samples.jsonl
```

</div>
</details>

<details><summary>⌨️ More command-line flags <i>:: click to expand ::</i></summary>
<div>

- `--parallel`: by default half of the cores
- `--base-only` (store_ture): only run base HumanEval tests
- `--i-just-wanna-run`: force a re-run

</div>
</details>

The output should be like (below is GPT-4 greedy decoding example):

```
Computing expected output...
Expected outputs computed in 15.18s
Reading samples...
164it [00:04, 37.79it/s]
Evaluating samples...
100%|██████████████████████████████████████████| 164/164 [00:03<00:00, 44.75it/s]
Base
{'pass@1': 0.8841463414634146}
Base + Extra
{'pass@1': 0.768}
```

- `Base` is the `pass@k` for the original HumanEval
- `Base + Extra` is the `pass@k` for the our **HumanEval+** (with extra tests)
- The "k" includes `[1, 10, 100]` where k values `<=` the sample size will be used
- A cache file named like `samples_eval_results.jsonl` will be cached. Remove it to re-run the evaluation

## Test input generation using EvalPlus

Please check `evalplus/inputgen.py`.

## Useful tools

We provide some useful tools for curation, visualization, and analysis of the EvalPlus datasets in the `tools/` directory.
To use these tools, please first install the repository from GitHub:

```bash
git clone https://github.com/evalplus/evalplus.git
cd evalplus
pip install -r tools/requirements.txt
```
