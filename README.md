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
    <a href="#-documents">📚Documents</a> •
    <a href="#-llm-generated-code">💻LLM code</a> •
    <a href="#-citation">📜Citation</a> •
    <a href="#-acknowledgement">🙏Acknowledgement</a>
</p>

## About

EvalPlus is a rigorous evaluation framework for LLM4Code, with:

- ✨ **HumanEval+**: 80x more tests than the original HumanEval!
- ✨ **MBPP+**: 35x more tests than the original MBPP!
- ✨ **Evaluation framework**: our packages/images/tools can easily and safely evaluate LLMs on above benchmarks.

Why EvalPlus?

- ✨ **Precise evaluation & ranking**: See [our leaderboard](https://evalplus.github.io/leaderboard.html) for latest LLM rankings before & after rigorous evaluation.
- ✨ **Coding rigorousness**: Look at the score differences! esp. before and after using EvalPlus tests! Less drop is better as it means more rigorousness and less laxity in code generation; while a big drop means the generated code tends to be fragile.
- ✨ **Pre-generated samples**: EvalPlus accelerates LLM4Code research by open-sourcing [LLM-generated samples](#-LLM-generated-code) for various models -- no need to re-run the expensive benchmarks!

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

To quickly perform code generation and evaluation on HumanEval+:

```bash
pip install "evalplus[vllm]" --upgrade
evalplus.evaluate --model "deepseek-ai/deepseek-coder-6.7b-instruct" \
                  --dataset [humaneval|mbpp]                         \
                  --backend [vllm|hf|openai|anthropic|google]        \
                  --greedy
```

You can checkout the generation and results at `evalplus_results/[humaneval|mbpp]/`

<details><summary>⏬ Install nightly version <i>:: click to expand ::</i></summary>
<div>

```bash
pip install --upgrade "git+https://github.com/evalplus/evalplus.git"                     # without vLLM
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus@master" # with vLLM
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

## 📚 Documents

To learn more about how to use EvalPlus, please refer to:

- [Command Line Interface](./docs/cli.md)
- [Program Execution](./docs/execution.md)

## 💻 LLM-generated code

We also share pre-generated code samples from LLMs we have [evaluated](https://evalplus.github.io/leaderboard.html):

- **HumanEval+**: See the attachment of our [v0.1.0 release](https://github.com/evalplus/evalplus/releases/tag/v0.1.0).
- **MBPP+**: See the attachment of our [v0.2.0 release](https://github.com/evalplus/evalplus/releases/tag/v0.2.0).

Each sample file is packaged in a zip file named like `${model_name}_temp_${temperature}.zip`.
You can unzip them to a folder named like `${model_name}_temp_${temperature}` and run the evaluation from scratch with:

```bash
evalplus.evaluate --dataset humaneval --samples ${model_name}_temp_${temperature}
```

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
