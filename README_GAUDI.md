# EvalPlus with Intel Gaudi

This guide provides instructions on how to run EvalPlus with Intel Gaudi.

## Prerequisites

- Python 3.8 or higher
- PyTorch
- Habana Frameworks
- Transformers library from Hugging Face
- Optimum Habana

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/nprotasov/evalplus_gaudi.git
    cd evalplus_gaudi
    ```

2. Install the required packages:
    ```bash
    pip3 install -e .
    pip3 install -r requirements-gaudi.txt
    ```

3. If you want to use vLLM backend install vLLM:
    ```bash
    git clone https://github.com/HabanaAI/vllm-fork.git
    cd vllm-fork
    python setup.py develop 
    ```

## Running EvalPlus

To use Hugging Face Gaudi backend use: --backend hf_gaudi