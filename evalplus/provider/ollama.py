import json
from typing import List, Optional
from evalplus.gen.util.ollama_request import make_request
from evalplus.provider.base import DecoderBase
from evalplus.provider.utility import concurrent_call

class OllamaChatDecoder(DecoderBase):
    def __init__(self, name: str, base_url=None, num_ctx: Optional[int] = None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.base_url = base_url
        self.num_ctx = num_ctx
        self.max_new_tokens = -1  # In Ollama -1 means unlimited. -2 the context-length is the limit. It also accepts any int values as a limit similar to tokens

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200, num_ctx: Optional[int] = None
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        batch_size = min(self.batch_size, num_samples)
        prompt = self.instruction_prefix + f"\n```python\n{prompt.strip()}\n```"

        return self._codegen_api_batch(prompt, batch_size)

    def _codegen_api_batch(self, prompt: str, batch_size: int, num_ctx: Optional[int] = None) -> List[str]:
        responses = [
            make_request(
                model=self.name,
                prompt=prompt,
                max_tokens=self.max_new_tokens,
                temperature=self.temperature,
                num_ctx=self.num_ctx
            ) for _ in range(batch_size)
        ]
        return responses

    def _codegen_batch_via_concurrency(self, prompt: str, batch_size: int) -> List[str]:
        batches = concurrent_call(
            batch_size, self._codegen_api_batch, prompt, batch_size=1
        )
        return [b[0] for b in batches]

    def is_direct_completion(self) -> bool:
        return False
