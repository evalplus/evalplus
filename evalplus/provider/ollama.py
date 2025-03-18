import os
from typing import List, Optional

import ollama


from evalplus.gen.util import ollama_request
from evalplus.provider.base import DecoderBase


class OllamaChatDecoder(DecoderBase):
    def __init__(self, name: str, base_url=None, num_ctx: Optional[int] = None, temperature: Optional[float] = 0.7, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.base_url = base_url
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.max_new_tokens = -1  # In Ollama -1 means unlimited. -2 the context-length is the limit. It also accepts any int values as a limit similar to tokens

    def codegen(self, prompt: str, do_sample: bool = True, num_samples: int = 200, num_ctx: Optional[int] = None, temperature: Optional[float] = 0.7) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        
        batch_size = min(self.batch_size, num_samples)
        if not do_sample:
            assert batch_size == 1, "Sampling only supports batch size of 1"

        # Create a prompt that includes the instruction prefix and wraps the code in a Python code block
        full_prompt = self.instruction_prefix + f"\n```python\n{prompt.strip()}\n```\n"
        
        # Use make_auto_request with streaming enabled
        response = ollama_request.make_auto_request(
            model=self.name,
            prompt=full_prompt,
            max_tokens=self.max_new_tokens,
            temperature=self.temperature,
            num_ctx=self.num_ctx,
            n=batch_size,
            stream=True  # Enable streaming
        )
        
        outputs = []
        if "message" in response:
            outputs.append(response["message"]["content"])
        else:
            print(f"Unexpected response format: {response}")
        
        return outputs

    def is_direct_completion(self) -> bool:
        return False
