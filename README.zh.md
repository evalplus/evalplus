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
    <a href="https://github.com/evalplus/evalplus/blob/master/README.md">English</a> •
    <b>简体中文</b>
</p>

<p align="center">
    <a href="#-关于">📙关于</a> •
    <a href="#-快速开始">🔥快速开始</a> •
    <a href="#-llm-后端">🚀LLM 后端</a> •
    <a href="#-文档指南">📚文档指南</a> •
    <a href="#-引用">📜引用</a> •
    <a href="#-致谢">🙏致谢</a>
</p>

## 📢 最新动态

哪些团队正在使用 EvalPlus 数据集？EvalPlus 已被众多主流大语言模型（LLM）团队广泛采用，包括：

* [Meta Llama 3.1 与 3.3](https://ai.meta.com/blog/meta-llama-3-1/)
* [Allen AI TÜLU 1/2/3](https://github.com/allenai/open-instruct/blob/main/docs/tulu1_tulu2.md#benchmark-based-eval)
* [Qwen2.5-Coder](https://qwenlm.github.io/blog/qwen2.5-coder-family/)
* [CodeQwen 1.5](https://qwenlm.github.io/blog/codeqwen1.5/)
* [DeepSeek-Coder V2](https://arxiv.org/pdf/2406.11931)
* [Qwen2](https://arxiv.org/pdf/2407.10671)
* [Snowflake Arctic](https://www.snowflake.com/en/data-cloud/arctic/)
* [StarCoder2](https://arxiv.org/pdf/2402.19173)
* [Magicoder](https://arxiv.org/pdf/2312.02120)
* [WizardCoder](https://arxiv.org/pdf/2306.08568)

以下记录了 EvalPlus 的重要版本更新：

- **[2024-10-20 `v0.3.1`]**：EvalPlus `v0.3.1` 正式发布！核心亮点：*(i)* 通过 EvalPerf 评测代码运行效率；*(ii)* 单条命令全流程运行：代码生成 + 后处理 + 评测；*(iii)* 支持 Google Gemini、Anthropic 等更多推理后端。
- **[2024-06-09 pre `v0.3.0`]**：改进了 MBPP+ 任务（ID：459、102、559）的标准参考解答（ground-truth solutions）。鸣谢 [EvalArena](https://github.com/crux-eval/eval-arena)。
- **[2024-04-17 pre `v0.3.0`]**：移除部分存在缺陷的任务（从 399 个精简至 378 个任务），将 MBPP+ 升级至 `v0.2.0`，预计可带来约 4 个百分点的 pass@1 提升。

<details><summary>早期动态 <i>:: 点击展开 ::</i></summary>
<div>

- ([`v0.2.1`](https://github.com/evalplus/evalplus/releases/tag/v0.2.1)) 现已支持通过 [bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness) 使用 EvalPlus 数据集！修复 HumanEval+ 标准解答（32）。
- ([`v0.2.0`](https://github.com/evalplus/evalplus/releases/tag/v0.2.0)) MBPP+ 正式发布！修复 HumanEval 契约与输入（0/3/9/148/114/1/2/99/28/32/35/160）。
- ([`v0.1.7`](https://github.com/evalplus/evalplus/releases/tag/v0.1.7)) [排行榜（Leaderboard）](https://evalplus.github.io/leaderboard.html)上线；修复 HumanEval+ 契约与输入（32/166/126/6）。
- ([`v0.1.6`](https://github.com/evalplus/evalplus/releases/tag/v0.1.6)) 支持可配置且默认保守的超时设置；修复 HumanEval+ 契约与标准解答（129/148/75/53/0/3/9/140）。
- ([`v0.1.5`](https://github.com/evalplus/evalplus/releases/tag/v0.1.5)) 发布 HumanEval+ mini，可在样本量庞大时实现极速评测！
- ([`v0.1.1`](https://github.com/evalplus/evalplus/releases/tag/v0.1.1)) 用户体验优化：提升评测速度、发布 PyPI 软件包与 Docker 镜像等。
- ([`v0.1.0`](https://github.com/evalplus/evalplus/releases/tag/v0.1.0)) HumanEval+ 正式发布！

</div>
</details>


## 📙 关于

EvalPlus 是一个面向代码大模型（LLM4Code）的严密评测框架，包含：

- ✨ **HumanEval+**：测试用例数量达到原版 HumanEval 的 80 倍！
- ✨ **MBPP+**：测试用例数量达到原版 MBPP 的 35 倍！
- ✨ **EvalPerf**：专注于评测大语言模型生成代码的执行效率！
- ✨ **一站式评测框架**：借助我们提供的软件包、镜像与工具，能够简便且安全地在上述基准上评测各类大语言模型。

为什么选择 EvalPlus？

- ✨ **精准评测**：查看[官方排行榜](https://evalplus.github.io/leaderboard.html)，对比严密评测前后的最新大模型排名变化。
- ✨ **代码严密性度量**：关注使用 EvalPlus 测试集前后的分数降幅！降幅越小，说明模型生成的代码越严密健壮；降幅越大，则表明生成的代码越脆弱易错。
- ✨ **代码效率评测**：除正确性外，我们的 EvalPerf 数据集通过压力测试级的编程任务与测试输入，全面评估大模型生成代码的运行效率。

想了解更多技术细节？欢迎阅读我们的论文与相关资料：

- **EvalPlus**：[NeurIPS'23 论文](https://openreview.net/forum?id=1qvx610Cu7)、[演讲幻灯片](https://docs.google.com/presentation/d/1eTxzUQG9uHaU13BGhrqm4wH5NmMZiM3nI0ezKlODxKs)、[海报（Poster）](https://jw-liu.xyz/assets/pdf/EvalPlus_Poster.pdf)、[排行榜](https://evalplus.github.io/leaderboard.html)
- **EvalPerf**：[COLM'24 论文](https://openreview.net/forum?id=IBCBMeAhmC)、[海报（Poster）](https://jw-liu.xyz/assets/pdf/jiawei-colm-evalperf-poster.pdf)、[技术文档](./docs/evalperf.md)、[排行榜](https://evalplus.github.io/evalperf.html)


## 🔥 快速开始

### 代码正确性评测：HumanEval(+) 或 MBPP(+)

```bash
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus"
# 或运行 `pip install "evalplus[vllm]" --upgrade` 安装最新稳定版本

evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend vllm                         \
                  --greedy
```

<details><summary>🛡️ 在 Docker 容器中安全执行代码 <i>:: 点击展开 ::</i></summary>
<div>

```bash
# 本地代码生成
evalplus.codegen --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                 --dataset humaneval                    \
                 --backend vllm                         \
                 --greedy

# 在 Docker 容器内执行评测
docker run --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval                                     \
           --samples /app/humaneval/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_0.0.jsonl
```

</div>
</details>

### 代码效率评测：EvalPerf（仅限 *nix 系统）

```bash
pip install --upgrade "evalplus[perf,vllm] @ git+https://github.com/evalplus/evalplus"
# 或运行 `pip install "evalplus[perf,vllm]" --upgrade` 安装最新稳定版本

sudo sh -c 'echo 0 > /proc/sys/kernel/perf_event_paranoid' # 启用 perf 性能计数器
evalplus.evalperf --model "ise-uiuc/Magicoder-S-DS-6.7B" --backend vllm
```

<details><summary>🛡️ 在 Docker 容器中安全执行代码 <i>:: 点击展开 ::</i></summary>
<div>

```bash
# 本地代码生成
evalplus.codegen --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                 --dataset evalperf                     \
                 --backend vllm                         \
                 --temperature 1.0                      \
                 --n-samples 100

# 在 Docker 容器内执行评测
sudo sh -c 'echo 0 > /proc/sys/kernel/perf_event_paranoid' # 启用 perf 性能计数器
docker run --cap-add PERFMON --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evalperf --samples /app/evalperf/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_1.0.jsonl
```

</div>
</details>

## 🚀 LLM 后端

### HuggingFace 模型

- `transformers` 后端：

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend hf                           \
                  --greedy
```

> [!Note]
>
> EvalPlus 对基座模型（base models）与对话模型（chat models）使用不同的提示词模板。
> 当使用 `hf`/`vllm` 作为后端时，默认会根据 `tokenizer.chat_template` 自动检测模型类型。
> 对于其他后端，则仅支持对话模式（chat mode）。
>
> 因此，如果您的基座模型自带了 `tokenizer.chat_template`，请务必添加 `--force-base-prompt` 参数，以避免被误作为对话模式进行评测。

<details><summary>启用 Flash Attention 2 <i>:: 点击展开 ::</i></summary>
<div>

```bash
# 安装 Flash Attention 2
pip install packaging ninja
pip install flash-attn --no-build-isolation
# 注：如遇到安装问题，建议从 https://github.com/Dao-AILab/flash-attention/releases 下载预编译 wheel 包

# 使用 FA2 运行评测
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B"         \
                  --dataset [humaneval|mbpp]                     \
                  --backend hf                                   \
                  --attn-implementation [flash_attention_2|sdpa] \
                  --greedy
```

</div>
</details>

- `vllm` 后端：

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --backend vllm                         \
                  --tp [TENSOR_PARALLEL_SIZE]            \
                  --greedy
```

- `openai` 兼容服务端（例如 [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)）：

```bash
# OpenAI 模型
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

# vLLM 服务端
# 首先启动 vLLM 服务：https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset [humaneval|mbpp]             \
                  --base-url http://localhost:8000/v1    \
                  --backend openai --greedy

# GPTQModel
evalplus.evaluate --model "ModelCloud/Llama-3.2-1B-Instruct-gptqmodel-4bit-vortex-v1" \
                  --dataset [humaneval|mbpp]                                          \
                  --backend gptqmodel --greedy
```

### OpenAI 模型

- 从 [OpenAI Console](https://platform.openai.com/) 获取 OpenAI API 密钥

```bash
export OPENAI_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "gpt-4o"            \
                  --dataset [humaneval|mbpp]  \
                  --backend openai            \
                  --greedy
```

### Anthropic 模型

- 从 [Anthropic Console](https://console.anthropic.com/) 获取 Anthropic API 密钥

```bash
export ANTHROPIC_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "claude-3-haiku-20240307" \
                  --dataset [humaneval|mbpp]        \
                  --backend anthropic               \
                  --greedy
```

### Google Gemini 模型

- 从 [Google AI Studio](https://aistudio.google.com/) 获取 Gemini API 密钥

```bash
export GOOGLE_API_KEY="[YOUR_API_KEY]"
evalplus.evaluate --model "gemini-1.5-pro"    \
                  --dataset [humaneval|mbpp]  \
                  --backend google            \
                  --greedy
```

### Amazon Bedrock 模型

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

```bash
export BEDROCK_ROLE_ARN="[BEDROCK_ROLE_ARN]"
evalplus.evaluate --model "anthropic.claude-3-5-sonnet-20241022-v2:0" \
                  --dataset [humaneval|mbpp]                          \
                  --backend bedrock                                   \
                  --greedy
```

### Ollama 后端

- [Ollama](https://ollama.com/)

```bash
evalplus.evaluate --model "mistral:7b" \
                  --dataset [humaneval|mbpp]          \
                  --backend ollama                    \
                  --base-url http://localhost:11434/v1 \
                  --greedy
```

### Intel® Gaudi® 加速器

- [Intel® Gaudi®](https://docs.habana.ai/en/latest/index.html)

如需在 Intel Gaudi 上运行 `hf` 后端，请先安装 [optimum-habana](https://github.com/huggingface/optimum-habana)：

```bash
pip install git+https://github.com/huggingface/optimum-habana.git
evalplus.evaluate --model "qwen/CodeQwen1.5-7B-Chat" \
                  --dataset [humaneval|mbpp]         \
                  --backend hf_gaudi                 \
                  --greedy                           \
                  --torch_compile
```
或使用延迟执行模式（Lazy Mode）：
```bash
PT_HPU_LAZY_MODE=1 evalplus.evaluate --model "qwen/CodeQwen1.5-7B-Chat" \
                  --dataset [humaneval|mbpp]                            \
                  --backend hf_gaudi                                    \
                  --greedy
```

如需在 Intel Gaudi 上运行 `vllm` 后端，请先安装 [HabanaAI vllm](https://github.com/HabanaAI/vllm-fork)：

```bash
git clone https://github.com/HabanaAI/vllm-fork.git
cd vllm-fork
git checkout habana_main
pip install --upgrade pip
pip install -r requirements-hpu.txt
python setup.py develop
```
随后运行：
```bash
PT_HPU_LAZY_MODE=1 evalplus.evaluate --model "qwen/CodeQwen1.5-7B-Chat" \
                  --dataset [humaneval|mbpp]                            \
                  --backend vllm                                        \
                  --greedy
```
您可以在 `evalplus_results/[humaneval|mbpp]/` 目录下查看生成的代码与评测结果。

<details><summary>⏬ 将 EvalPlus 作为本地仓库使用？ <i>:: 点击展开 ::</i></summary>
<div>

```bash
git clone https://github.com/evalplus/evalplus.git
cd evalplus
export PYTHONPATH=$PYTHONPATH:$(pwd)
pip install -r requirements.txt
```

</div>
</details>

## 📚 文档指南

欲了解更多关于如何使用 EvalPlus 的详细说明，请参阅：

- [EvalPlus 命令行指南](./docs/cli.md)
- [EvalPerf 性能评测说明](./docs/evalperf.md)
- [程序执行机制](./docs/execution.md)

## 📜 引用

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

## 🙏 致谢

- [HumanEval](https://github.com/openai/human-eval)
- [MBPP](https://github.com/google-research/google-research/tree/master/mbpp)

---

> _注：本中文文档由社区志愿者翻译与维护，旨在降低中文开发者的阅读门槛。如与英文原版存在差异或更新延迟，请以英文原版 [README.md](https://github.com/evalplus/evalplus/blob/master/README.md) 为唯一权威标准（Single Source of Truth）。_
