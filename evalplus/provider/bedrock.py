import datetime
import os
from typing import Dict, List

import boto3
from botocore.config import Config

from evalplus.provider.base import DecoderBase
from evalplus.provider.utility import concurrent_call

BEDROCK_CONFIG = Config(retries={"max_attempts": 100, "mode": "standard"})


class AutoRefreshBedrockCaller:
    def __init__(self, role_arn, region_name):
        self.role_arn = role_arn
        self.region_name = region_name
        self.session_name = "BedrockSession"
        self.session = boto3.Session()
        self.sts_client = self.session.client("sts", region_name=region_name)
        self.bedrock_client = boto3.client(
            "bedrock-runtime", config=BEDROCK_CONFIG, region_name=region_name
        )
        self.expiration = None
        self.refresh_credentials()

    def refresh_credentials(self):
        assumed_role = self.sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.session_name,
            DurationSeconds=12 * 60 * 60,
        )
        credentials = assumed_role["Credentials"]
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=self.region_name,
            config=BEDROCK_CONFIG,
        )
        self.expiration = credentials["Expiration"]

    def _refresh_guard(self):
        if self.expiration is None or datetime.datetime.now(
            datetime.timezone.utc
        ) > self.expiration - datetime.timedelta(minutes=10):
            self.refresh_credentials()

    def converse(self, *arg, **kwargs):
        self._refresh_guard()
        return self.bedrock_client.converse(*arg, **kwargs)


BEDROCK_ROLE_ARN = os.getenv("BEDROCK_ROLE_ARN", None)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class BedrockDecoder(DecoderBase):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)

    def _call_one(self, messages: List[Dict[str, str]]) -> str:
        assert (
            BEDROCK_ROLE_ARN
        ), "Please specify BEDROCK_ROLE_ARN via environment variable"
        self.client = AutoRefreshBedrockCaller(
            role_arn=BEDROCK_ROLE_ARN, region_name=AWS_REGION
        )

        response = self.client.converse(
            modelId=self.name,
            messages=messages,
            inferenceConfig={
                "maxTokens": self.max_new_tokens,
                "temperature": self.temperature,
                "topP": 0.95,
            },
        )

        return response["output"]["message"]["content"][0]["text"]

    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        if do_sample:
            assert self.temperature > 0, "Temperature must be positive for sampling"
        batch_size = min(self.batch_size, num_samples)
        prompt = self.instruction_prefix + f"\n```python\n{prompt.strip()}\n```"
        messages = [{"role": "user", "content": [{"text": prompt.strip()}]}]

        return concurrent_call(batch_size, self._call_one, messages)

    def is_direct_completion(self) -> bool:
        return False
