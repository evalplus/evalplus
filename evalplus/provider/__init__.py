from evalplus.provider.base import DecoderBase


def make_model(
    model: str,
    backend: str,
    dataset: str,
    batch_size: int = 1,
    temperature: float = 0.0,
    force_base_prompt: bool = False,
    # instruction model only
    instruction_prefix=None,
    response_prefix=None,
    # non-server only
    dtype="bfloat16",
    trust_remote_code=False,
    # vllm only
    tp=1,
    # openai only
    base_url=None,
    # hf only
    attn_implementation="eager",
) -> DecoderBase:
    if backend == "vllm":
        from evalplus.provider.vllm import VllmDecoder

        return VllmDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            dataset=dataset,
            force_base_prompt=force_base_prompt,
            tensor_parallel_size=tp,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
            trust_remote_code=trust_remote_code,
            dtype=dtype,
        )
    elif backend == "hf":
        from evalplus.provider.hf import HuggingFaceDecoder

        return HuggingFaceDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            dataset=dataset,
            force_base_prompt=force_base_prompt,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
            attn_implementation=attn_implementation,
            trust_remote_code=trust_remote_code,
            dtype=dtype,
        )
    elif backend == "openai":
        from evalplus.provider.openai import OpenAIChatDecoder

        assert not force_base_prompt, f"{backend} backend does not serve base model"
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

        assert not force_base_prompt, f"{backend} backend does not serve base model"
        return AnthropicDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
    elif backend == "google":
        from evalplus.provider.google import GeminiDecoder

        assert not force_base_prompt, f"{backend} backend does not serve base model"
        return GeminiDecoder(
            name=model,
            batch_size=batch_size,
            temperature=temperature,
            instruction_prefix=instruction_prefix,
            response_prefix=response_prefix,
        )
