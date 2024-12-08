# `EvalPlus(📖) => 📚`

<p align="center">
    <a href="https://evalplus.github.io"><img src="https://img.shields.io/badge/%F0%9F%8F%86-leaderboard-8A2BE2"></a>
    <a href="https://openreview.net/forum?id=1qvx610Cu7"><img src="https://img.shields.io/badge/EvalPlus-NeurIPS'23-a55fed.svg"></a>
    <a href="https://openreview.net/forum?id=IBCBMeAhmC"><img src="https://img.shields.io/badge/EvalPerf-COLM'24-a55fed.svg"></a>
    <a href="https://huggingface.co/evalplus/"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-evalplus-%23ff8811.svg"></a>
    <a href="https://pypi.org/project/evalplus/"><img src="https://img.shields.io/pypi/v/evalplus?color=g"></a>
    <a href="https://hub.docker.com/r/ganler/evalplus" title="Docker"><img src="https://img.shields.io/docker/image-size/ganler/evalplus"></a>
</p>

<p align="center">
    <a href="#-about">📙About</a> •
    <a href="#-quick-start">🔥Quick Start</a> •
    <a href="#-llm-backends">🚀LLM Backends</a> •
    <a href="#-documents">📚Documents</a> •
    <a href="#-citation">📜Citation</a> •
    <a href="#-acknowledgement">🙏Acknowledgement</a>
</p>

## 📢 News

Who's using EvalPlus datasets? EvalPlus has been used by various LLM teams, including:

* [Meta Llama 3.1 and 3.3](https://ai.meta.com/blog/meta-llama-3-1/)
* [Allen AI TÜLU 1/2/3](https://github.com/allenai/open-instruct/blob/main/docs/tulu1_tulu2.md#benchmark-based-eval)
* [Qwen2.5-Coder](https://qwenlm.github.io/blog/qwen2.5-coder-family/)
* [CodeQwen 1.5](https://qwenlm.github.io/blog/codeqwen1.5/)
* [DeepSeek-Coder V2](https://arxiv.org/pdf/2406.11931)
* [Qwen2](https://arxiv.org/pdf/2407.10671)
* [Snowflake Arctic](https://www.snowflake.com/en/data-cloud/arctic/)
* [StarCoder2](https://arxiv.org/pdf/2402.19173)
* [Magicoder](https://arxiv.org/pdf/2312.02120)
* [WizardCoder](https://arxiv.org/pdf/2306.08568)

Below tracks the notable updates of EvalPlus:

- **[2024-10-20 `v0.3.1`]**: EvalPlus `v0.3.1` is officially released! Highlights: *(i)* Code efficiency evaluation via EvalPerf, *(ii)* one command to run all: generation + post-processing + evaluation, *(iii)* support for more inference backends such as Google Gemini & Anthropic, etc.
- **[2024-06-09 pre `v0.3.0`]**: Improved ground-truth solutions for MBPP+ tasks (IDs: 459, 102, 559). Thanks to [EvalArena](https://github.com/crux-eval/eval-arena).
- **[2024-04-17 pre `v0.3.0`]**: MBPP+ is upgraded to `v0.2.0` by removing some broken tasks (399 -> 378 tasks). ~4pp pass@1 improvement could be expected.

<details><summary>Earlier news <i>:: click to expand ::</i></summary>
<div>

- ([`v0.2.1`](https://github.com/evalplus/evalplus/releases/tag/v0.2.1)) You can use EvalPlus datasets via [bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness)! HumanEval+ oracle fixes (32).
- ([`v0.2.0`](https://github.com/evalplus/evalplus/releases/tag/v0.2.0)) MBPP+ is released! HumanEval contract & input fixes (0/3/9/148/114/1/2/99/28/32/35/160).
- ([`v0.1.7`](https://github.com/evalplus/evalplus/releases/tag/v0.1.7)) [Leaderboard](https://evalplus.github.io/leaderboard.html) release; HumanEval+ contract and input fixes (32/166/126/6)
- ([`v0.1.6`](https://github.com/evalplus/evalplus/releases/tag/v0.1.6)) Configurable and by-default-conservative timeout settings; HumanEval+ contract & ground-truth fixes (129/148/75/53/0/3/9/140)
- ([`v0.1.5`](https://github.com/evalplus/evalplus/releases/tag/v0.1.5)) HumanEval+ mini is released for ultra-fast evaluation when you have too many samples!
- ([`v0.1.1`](https://github.com/evalplus/evalplus/releases/tag/v0.1.1)) Optimizing user experiences: evaluation speed, PyPI package, Docker, etc.
- ([`v0.1.0`](https://github.com/evalplus/evalplus/releases/tag/v0.1.0)) HumanEval+ is released!

</div>
</details>


## 📙 About

EvalPlus is a rigorous evaluation framework for LLM4Code, with:

- ✨ **HumanEval+**: 80x more tests than the original HumanEval!
- ✨ **MBPP+**: 35x more tests than the original MBPP!
- ✨ **EvalPerf**: evaluating the efficiency of LLM-generated code!
- ✨ **Framework**: our packages/images/tools can easily and safely evaluate LLMs on above benchmarks.

Why EvalPlus?

- ✨ **Precise evaluation**: See [our leaderboard](https://evalplus.github.io/leaderboard.html) for latest LLM rankings before & after rigorous evaluation.
- ✨ **Coding rigorousness**: Look at the score differences! esp. before & after using EvalPlus tests! Less drop means more rigorousness in code generation; while a bigger drop means the generated code tends to be fragile.
- ✨ **Code efficiency**: Beyond correctness, our EvalPerf dataset evaluates the efficiency of LLM-generated code via performance-exercising coding tasks and test inputs.

Want to know more details? Read our papers & materials!

- **EvalPlus**: [NeurIPS'23 paper](https://openreview.net/forum?id=1qvx610Cu7), [Slides](https://docs.google.com/presentation/d/1eTxzUQG9uHaU13BGhrqm4wH5NmMZiM3nI0ezKlODxKs), [Poster](https://jw-liu.xyz/assets/pdf/EvalPlus_Poster.pdf), [Leaderboard](https://evalplus.github.io/leaderboard.html)
- **EvalPerf**: [COLM'24 paper](https://openreview.net/forum?id=IBCBMeAhmC), [Poster](https://jw-liu.xyz/assets/pdf/jiawei-colm-evalperf-poster.pdf), [Documentation](./docs/evalperf.md), [Leaderboard](https://evalplus.github.io/evalperf.html)


## 🔥 Quick Start

### Code Correctness Evaluation: HumanEval(+) or MBPP(+)

```bash
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus"
# Or `pip install "evalplus[vllm]" --upgrade` for the latest stable release

evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend vllm                         \
                  --greedy
```

<details><summary>🛡️ Safe code execution within Docker <i>:: click to expand ::</i></summary>
<div>

```bash
# Local generation
evalplus.codegen --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                 --dataset humaneval                    \
                 --backend vllm                         \
                 --greedy

# Code execution within Docker
docker run --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval                                     \
           --samples /app/humaneval/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_0.0.jsonl
```

</div>
</details>

### Code Efficiency Evaluation: EvalPerf (*nix only)

```bash
pip install --upgrade "evalplus[perf,vllm] @ git+https://github.com/evalplus/evalplus"
# Or `pip install "evalplus[perf,vllm]" --upgrade` for the latest stable release

sudo sh -c 'echo 0 > /proc/sys/kernel/perf_event_paranoid' # Enable perf
evalplus.evalperf --model "ise-uiuc/Magicoder-S-DS-6.7B" --backend vllm
```

<details><summary>🛡️ Safe code execution within Docker <i>:: click to expand ::</i></summary>
<div>

```bash
# Local generation
evalplus.codegen --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                 --dataset evalperf                     \
                 --backend vllm                         \
                 --temperature 1.0                      \
                 --n-samples 100

# Code execution within Docker
sudo sh -c 'echo 0 > /proc/sys/kernel/perf_event_paranoid' # Enable perf
docker run --cap-add PERFMON --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evalperf --samples /app/evalperf/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_1.0.jsonl
```

</div>
</details>

## 🚀 LLM Backends

### HuggingFace models

- `transformers` backend:

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend hf                           \
                  --greedy
```

> [!Note]
>
> EvalPlus uses different prompts for base and chat models.
> By default it is detected by `tokenizer.chat_template` when using `hf`/`vllm` as backend.
> For other backends, only chat mode is allowed.
>
> Therefore, if your base models come with a `tokenizer.chat_template`,
> please add `--force-base-prompt` to avoid being evaluated
> in a chat mode.

<details><summary>Enable Flash Attention 2 <i>:: click to expand ::</i></summary>
<div>

```bash
# Install Flash Attention 2
pip install packaging ninja
pip install flash-attn --no-build-isolation
# Note: if you have installation problem, consider using pre-built
# wheels from https://github.com/Dao-AILab/flash-attention/releases

# Run evaluation with FA2
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B"         \
                  --dataset [humaneval|mbpp]                     \
                  --backend hf                                   \
                  --attn-implementation [flash_attention_2|sdpa] \
                  --greedy
```

</div>
</details>

- `vllm` backend:

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend vllm                         \
                  --tp [TENSOR_PARALLEL_SIZE]            \
                  --greedy
```

- `openai` compatible servers (e.g., [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)):

```bash
# OpenAI models
export OPENAI_API_KEY="{KEY}" # https://platform.openai.com/settings/organization/api-keys
evalplus.evaluate --model "gpt-4o-2024-08-06"  \
                  --dataset [humaneval|mbpp]   \
                  --backend openai --greedy

# DeepSeek
export OPENAI_API_KEY="{KEY}" # https://platform.deepseek.com/api_keys
evalplus.evaluate --model "deepseek-chat"              \
                  --dataset [humaneval|mbpp]           \
                  --base-url https://api.deepseek.com  \
                  --backend openai --greedy

# Grok
export OPENAI_API_KEY="{KEY}" # https://console.x.ai/
evalplus.evaluate --model "grok-beta"             \
                  --dataset [humaneval|mbpp]      \
                  --base-url https://api.x.ai/v1  \
                  --backend openai --greedy

# vLLM server
# First, launch a vLLM server: https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --base-url http://localhost:8000/v1    \
                  --backend openai --greedy

# GPTQModel
evalplus.evaluate --model "ModelCloud/Llama-3.2-1B-Instruct-gptqmodel-4bit-vortex-v1" \
                  --dataset [humaneval|mbpp]                                          \
                  --backend gptqmodel --greedy
```

### OpenAI models

- Access OpenAI APIs from [OpenAI Console](https://platform.openai.com/)

```bash
export OPENAI_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "gpt-4o"            \
                  --dataset [humaneval|mbpp]  \
                  --backend openai            \
                  --greedy
```

### Anthropic models

- Access Anthropic APIs from [Anthropic Console](https://console.anthropic.com/)

```bash
export ANTHROPIC_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "claude-3-haiku-20240307" \
                  --dataset [humaneval|mbpp]        \
                  --backend anthropic               \
                  --greedy
```

### Google Gemini models

- Access Gemini APIs from [Google AI Studio](https://aistudio.google.com/)

```bash
export GOOGLE_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "gemini-1.5-pro"    \
                  --dataset [humaneval|mbpp]  \
                  --backend google            \
                  --greedy
```

### Amazon Bedrock models

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

```bash
export BEDROCK_ROLE_ARN="[BEDROCK_ROLE_ARN]"
evalplus.evaluate --model "anthropic.claude-3-5-sonnet-20241022-v2:0" \
                  --dataset [humaneval|mbpp]                          \
                  --backend bedrock                                   \
                  --greedy
```

You can checkout the generation and results at `evalplus_results/[humaneval|mbpp]/`

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

- [EvalPlus Commands](./docs/cli.md)
- [EvalPerf](./docs/evalperf.md)
- [Program Execution](./docs/execution.md)

## 📜 Citation

```bibtex
@inproceedings{evalplus,
  title = {Is Your Code Generated by Chat{GPT} Really Correct? Rigorous Evaluation of Large Language Models for Code Generation},
  author = {Liu, Jiawei and Xia, Chunqiu Steven and Wang, Yuyao and Zhang, Lingming},
  booktitle = {Thirty-seventh Conference on Neural Information Processing Systems},
  year = {2023},
  url = {https://openreview.net/forum?id=1qvx610Cu7},
}

@inproceedings{evalperf,
  title = {Evaluating Language Models for Efficient Code Generation},
  author = {Liu, Jiawei and Xie, Songrun and Wang, Junhao and Wei, Yuxiang and Ding, Yifeng and Zhang, Lingming},
  booktitle = {First Conference on Language Modeling},
  year = {2024},
  url = {https://openreview.net/forum?id=IBCBMeAhmC},
}
```

## 🙏 Acknowledgement

- [HumanEval](https://github.com/openai/human-eval)
- [MBPP](https://github.com/google-research/google-research/tree/master/mbpp)
