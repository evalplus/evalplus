import ast
import os
import random
import signal
import time
from typing import Dict, List

import openai

def handler(signum, frame):
    # swallow signum and frame
    raise Exception("end of time")

class ChatGPTEngine:
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY", "dummy")

    def request(self, config: Dict) -> Dict:
        ret = None
        while ret is None:
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(100)
                ret = openai.ChatCompletion.create(**config)
                signal.alarm(0)
            except openai.error.InvalidRequestError as e:
                print(e)
                signal.alarm(0)
            except openai.error.RateLimitError as e:
                print("Rate limit exceeded. Waiting...")
                signal.alarm(0)
                time.sleep(5)
            except openai.error.APIConnectionError as e:
                print("API connection error. Waiting...")
                signal.alarm(0)
                time.sleep(5)
            except Exception as e:
                print("Unknown error. Waiting...")
                print(e)
                signal.alarm(0)
                time.sleep(1)
        return ret
    
    def create_chatgpt_config(
        self,
        message: str,
        max_tokens: int,
        temperature: float = 0.8,
        batch_size: int = 1,
        system_message: str = "You are a helpful assistant.",
        model: str = "gpt-3.5-turbo",
    ) -> Dict:
        config = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": batch_size,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": message},
            ],
        }
        return config

    def _parse_ret(self, ret: Dict) -> str:
        output = ret["choices"][0]["message"]["content"]
        return output
