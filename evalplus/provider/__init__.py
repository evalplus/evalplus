from evalplus.provider.base import DecoderBase


def make_model(
    model: str,
    backend: str,
    dataset: str,
    batch_size: int = 1,
    temperature: float = 0.0,
    tp=1,
    base_url=None,
    instruction_prefix=None,
    response_prefix=None,
    attn_implementation="eager",
) -> DecoderBase:
    if backend == "vllm":
        from evalplus.provider.vllm import VllmDecoder

        return VllmDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            dataset=dataset,
            tensor_parallel_size=tp,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
    elif backend == "hf":
        from evalplus.provider.hf import HuggingFaceDecoder

        return HuggingFaceDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            dataset=dataset,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
            attn_implementation=attn_implementation,
        )
    elif backend == "openai":
        from evalplus.provider.openai import OpenAIChatDecoder

        return OpenAIChatDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            base_url=base_url,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
    elif backend == "anthropic":
        from evalplus.provider.anthropic import AnthropicDecoder

        return AnthropicDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
    elif backend == "google":
        from evalplus.provider.google import GeminiDecoder

        return GeminiDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
