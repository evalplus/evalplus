# `EvalPlus(📖) => 📚`

<p align="center">
    <a href="https://evalplus.github.io/leaderboard.html"><img src="https://img.shields.io/badge/%F0%9F%8F%86-leaderboard-8A2BE2"></a>
    <a href="https://openreview.net/forum?id=1qvx610Cu7"><img src="https://img.shields.io/badge/Paper-NeurIPS'23-a55fed.svg"></a>
    <a href="https://huggingface.co/evalplus/"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-evalplus-%23ff8811.svg"></a>
    <a href="https://pypi.org/project/evalplus/"><img src="https://img.shields.io/pypi/v/evalplus?color=g"></a>
    <a href="https://pepy.tech/project/evalplus"><img src="https://static.pepy.tech/badge/evalplus"></a>
    <a href="https://hub.docker.com/r/ganler/evalplus" title="Docker"><img src="https://img.shields.io/docker/image-size/ganler/evalplus"></a>
    <a href="https://github.com/evalplus/evalplus/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/evalplus"></a>
</p>


<p align="center">
    <a href="#-quick-start">🔥Quick Start</a> •
    <a href="#-llm-generated-code">💻LLM code</a> •
    <a href="#-useful-tools">🔨Tools</a> •
    <a href="#-citation">📜Citation</a> •
    <a href="#-acknowledgement">🙏Acknowledgement</a>
</p>

## About

EvalPlus is a rigorous evaluation framework for LLM4Code, with:

* ✨ **HumanEval+**: 80x more tests than the original HumanEval!
* ✨ **MBPP+**: 35x more tests than the original MBPP!
* ✨ **Evaluation framework**: our packages/images/tools can easily and safely evaluate LLMs on above benchmarks.

Why EvalPlus?

* ✨ **Precise evaluation & ranking**: See [our leaderboard](https://evalplus.github.io/leaderboard.html) for latest LLM rankings before & after rigorous evaluation.
* ✨ **Coding rigorousness**: Look at the score differences! esp. before and after using EvalPlus tests! Less drop is better as it means more rigorousness and less laxity in code generation; while a big drop means the generated code tends to be fragile.
* ✨ **Pre-generated samples**: EvalPlus accelerates LLM4Code research by open-sourcing [LLM-generated samples](#-LLM-generated-code) for various models -- no need to re-run the expensive benchmarks!

Want to know more details? Read our [**NeurIPS'23 paper**](https://openreview.net/forum?id=1qvx610Cu7) [![](https://img.shields.io/badge/Paper-NeurIPS'23-a55fed.svg)](https://openreview.net/forum?id=1qvx610Cu7) as well as our [**Google Slides**](https://docs.google.com/presentation/d/1eTxzUQG9uHaU13BGhrqm4wH5NmMZiM3nI0ezKlODxKs)!

> [!Important]
>
> 🚧 **MBPP+ update (`v0.1.0` to `v0.2.0`)**:
> We recently improved and stablized MBPP+ dataset by removing some tasks whose `test_list` is wrong (brought by the original MBPP dataset itself) to make it more reasonable to solve.
> In `v0.1.0` MBPP+ has 399 tasks while the new `v0.2.0` has 378 tasks.
> We also improved the oracle. Therefore, **using `v0.2.0` you might expect ~4pp pass@1 improvement** for both base and plus tests.

## 🔥 Quick Start

> [!Tip]
>
> EvalPlus ❤️ [bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness)!
> HumanEval+ and MBPP+ have been integrated to bigcode-evaluation-harness that you can also run EvalPlus datasets there!

To get started, please first setup the environment:

```bash
pip install evalplus --upgrade
```

<details><summary>⏬ Install nightly version <i>:: click to expand ::</i></summary>
<div>

```bash
pip install "git+https://github.com/evalplus/evalplus.git" --upgrade
```

</div>
</details>

<details><summary>⏬ Using EvalPlus as a local repo? <i>:: click to expand ::</i></summary>
<div>

```bash
git clone https://github.com/evalplus/evalplus.git
cd evalplus
export PYTHONPATH=$PYTHONPATH:$(pwd)
pip install -r requirements.txt
```

</div>
</details>


### Code generation

Implement the `GEN_SOLUTION` function by calling the LLM to produce the complete solution (include the code) and save the samples to `samples.jsonl`:

```python
from evalplus.data import get_[human_eval|mbpp]_plus, write_jsonl

samples = [
    dict(task_id=task_id, solution=GEN_SOLUTION(problem["prompt"]))
    for task_id, problem in get_[human_eval|mbpp]_plus().items()
]
write_jsonl("samples.jsonl", samples)
```

<details><summary>🤔 Structure of `problem`? <i>:: click to expand ::</i></summary>
<div>

* `task_id` is the identifier string for the task
* `entry_point` is name of the function
* `prompt` is the function signature with docstring
+ `canonical_solution` is the ground-truth implementation (re-implemented to fix bugs in HumanEval)
+ `base_input` is the test inputs in original HumanEval
+ `plus_input` is the test inputs brought by EvalPlus

</div>
</details>

> [!Note]
>
> **Expected Schema of `samples.jsonl`**
>
> 1. `task_id`: Task ID, which are the keys of `get_[human_eval|mbpp]_plus()`
> 2. `solution` (optional): Self-contained solution (usually including the prompt)
>    * Example: `{"task_id": "HumanEval/?", "solution": "def f():\n    return 1"}`
> 3. `completion` (optional): Function body without prompt
>    * Example: `{"task_id": "HumanEval/?", "completion": "    return 1"}`
>
> Only one of `solution` and `completion` is required. If both are provided, `solution` will be used.
> We also accept solutions in the form of directory, i.e., `--samples ${SAMPLE_DIR}` where `${SAMPLE_DIR}` is organized as: `${SAMPLE_DIR}/${TASK_ID}/{SAMPLE_ID}.py` (`${TASK_ID} = task_id.replace("/", "_")`).

### Code post-processing

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

### Code evaluation

You are strongly recommended to use a sandbox such as [docker](https://docs.docker.com/get-docker/):

```bash
docker run -v $(pwd):/app ganler/evalplus:latest --dataset [humaneval|mbpp] --samples samples.jsonl
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
> Do you use a very slow machine?
>
> LLM solutions are regarded as **failed** on timeout (and OOM etc.).
> Specifically, we set the timeout $T=\max(T_{base}, T_{gt}\times k)$, where:
>
> - $T_{base}$ is the minimal timeout (configurable by `--min-time-limit`; default to 1s);
> - $T_{gt}$ is the runtime of the ground-truth solutions (achieved via profiling);
> - $k$ is a configurable factor `--gt-time-limit-factor` (default to 4);
>
> If your machine is too slow and you are getting high-variance results, try to use larger $k$ and $T_{base}$.
>
> Additionally, you are **NOT** encouraged to make your test-bed over stressed while running evaluation.
> For example, using `--parallel 64` on a 4-core machine or doing something else during evaluation are bad ideas...

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

* `--parallel`: by default half of the cores
* `--base-only` (store_ture): only run base HumanEval tests
* `--i-just-wanna-run`: force a re-run

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

<details><summary>🤔 How long it would take? <i>:: click to expand ::</i></summary>
<div>

If you do greedy decoding where there is only one sample for each task, the evaluation should take just a few seconds.
When running 200 samples x 164 tasks x ~700+ tests, it can take around 2-10 minutes by using `--parallel 64` and `--test-details`.
Here are some tips to speed up the evaluation:

* Use `--parallel $(nproc)`
* Do **NOT** use `--test-details` if you just want to quickly get pass@k as `--test-details` will run all tests (700+ on average for each task), while without `--test-details` the testing for a sample stops immediately when it fails the first test.
* Use our pre-evaluated results (see [LLM-generated code](#-LLM-generated-code))
* Use HumanEval+ Mini

</div>
</details>

> [!Tip]
>
> 🚀 **Try out `HumanEvalPlus-Mini`!** which selects a *minimal* set of additional tests with the highest quality, achieving almost the same effectiveness of the full version. Just add a **`--mini`** flag, it can run 23+% faster! (even faster if you evaluate all tests without fail-stop with `--test-details`).
>
> ```bash
> docker run -v $(pwd):/app ganler/evalplus:latest --dataset humaneval --samples samples.jsonl --mini
> # ...Or locally ⚠️
> # evalplus.evaluate --dataset humaneval --samples samples.jsonl --mini
> ```


## 💻 LLM-generated code

We also share pre-generated code samples from LLMs we have [evaluated](https://evalplus.github.io/leaderboard.html):

* **HumanEval+**: See the attachment of our [v0.1.0 release](https://github.com/evalplus/evalplus/releases/tag/v0.1.0).
* **MBPP+**: See the attachment of our [v0.2.0 release](https://github.com/evalplus/evalplus/releases/tag/v0.2.0).

Each sample file is packaged in a zip file named like `${model_name}_temp_${temperature}.zip`.
You can unzip them to a folder named like `${model_name}_temp_${temperature}` and run the evaluation from scratch with:

```bash
evalplus.evaluate --dataset humaneval --samples ${model_name}_temp_${temperature}
```

## 🔨 Useful tools

To use these tools, please first install the repository from GitHub:

```bash
git clone https://github.com/evalplus/evalplus.git
cd evalplus
pip install -r tools/requirements.txt
```

### Code generation

You can use `codegen/generate.py` to performance code generation.
We currently support following backends:

* `vllm`: Set `--model` as Hugging Face model ID such as `microsoft/Phi-3-mini-128k-instruct`
* `hf`: HuggingFace Transformers; same way to setup `--model`
* `openai`: Configure `OPENAI_API_KEY`; one can configure `--base-url`
* `anthropic`: Configure `ANTHROPIC_API_KEY`
* `mistral`: Configure `MISTRAL_API_KEY`

```shell
python codegen/generate.py --model "mistralai/Mistral-7B-Instruct-v0.2" --greedy --root [result_path] --dataset [mbpp|humaneval] --backend [vllm]
```

To perform code generation using user-defined tasks and datasets:

```shell
# Override HumanEval datasets
HUMANEVAL_OVERRIDE_PATH="/path/to/HumanEvalPlus.jsonl.gz" python codegen/generate.py --model "mistralai/Mistral-7B-Instruct-v0.2" --greedy --root [result_path] --dataset humaneval --backend [vllm|hf|openai]
# Override MBPP datasets
MBPP_OVERRIDE_PATH="/path/to/MbppPlus.jsonl.gz" python codegen/generate.py --model "mistralai/Mistral-7B-Instruct-v0.2" --greedy --root [result_path] --dataset mbpp --backend [vllm|hf|openai]
```


### Test input generation using EvalPlus

Please check `evalplus/inputgen.py`.

## 📜 Citation

```bibtex
@inproceedings{evalplus,
  title = {Is Your Code Generated by Chat{GPT} Really Correct? Rigorous Evaluation of Large Language Models for Code Generation},
  author = {Liu, Jiawei and Xia, Chunqiu Steven and Wang, Yuyao and Zhang, Lingming},
  booktitle = {Thirty-seventh Conference on Neural Information Processing Systems},
  year = {2023},
  url = {https://openreview.net/forum?id=1qvx610Cu7},
}
```

## 🙏 Acknowledgement

- [HumanEval](https://github.com/openai/human-eval)
- [MBPP](https://github.com/google-research/google-research/tree/master/mbpp)
