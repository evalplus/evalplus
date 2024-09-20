import os
from typing import List

import openai

from evalplus.gen.util import openai_request
from evalplus.provider.base import DecoderBase


class OpenAIChatDecoder(DecoderBase):
    def __init__(self, name: str, base_url=None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "none"), base_url=base_url
        )

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        batch_size = min(self.batch_size, num_samples)
        message = self.instruction_prefix + f"\n```python\n{prompt.strip()}\n```"
        ret = openai_request.make_auto_request(
            self.client,
            message=message,
            model=self.name,
            max_tokens=self.max_new_tokens,
            temperature=self.temperature,
            n=batch_size,
        )

        outputs = []
        for item in ret.choices:
            outputs.append(item.message.content)

        return outputs

    def is_direct_completion(self) -> bool:
        return False
