import os
import time
from traceback import print_exc
from typing import List

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, ResourceExhausted

from evalplus.provider.base import DecoderBase


def make_request(
    client: genai.GenerativeModel,
    messages: List,
    temperature: float,
    n: int,
    max_new_tokens: int = 2048,
) -> genai.types.GenerateContentResponse:
    messages = [{"role": m["role"], "parts": [m["content"]]} for m in messages]
    response = client.generate_content(
        messages,
        generation_config=genai.types.GenerationConfig(
            candidate_count=n,
            max_output_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.95,
        ),
        safety_settings=[
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        ],
    )

    return response


def make_auto_request(*args, **kwargs) -> genai.types.GenerateContentResponse:
    ret = None
    while ret is None:
        try:
            ret = make_request(*args, **kwargs)
        except ResourceExhausted as e:
            print("Rate limit exceeded. Waiting...", e.message)
            time.sleep(10)
        except GoogleAPICallError as e:
            print(e.message)
            time.sleep(1)
        except Exception:
            print("Unknown error. Waiting...")
            print_exc()
            time.sleep(1)
    return ret


class GeminiDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.client = genai.GenerativeModel(name)

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        batch_size = min(self.batch_size, num_samples, 8)
        message = self.instruction_prefix + f"\n```python\n{prompt.strip()}\n```"
        replies = make_auto_request(
            self.client,
            [{"role": "user", "content": message}],
            n=batch_size,
            temperature=self.temperature,
            max_new_tokens=self.max_new_tokens,
        )

        if len(replies.candidates) != batch_size:
            print(
                f"WARNING: Expected {batch_size} outputs but got {len(replies.candidates)}"
            )

        ret_texts = []
        for candidate in replies.candidates:
            parts = candidate.content.parts
            if parts:
                ret_texts.append(parts[0].text)
            else:
                print("Empty response!")
                ret_texts.append("")
                print(f"{candidate.safety_ratings = }")

        return ret_texts + [""] * (batch_size - len(ret_texts))

    def is_direct_completion(self) -> bool:
        return False
