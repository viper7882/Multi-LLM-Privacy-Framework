import httpx
import openai
import os
import tiktoken

from typing import Any, Generator, List, Optional
from ..base import BaseLLM


class OpenAIClient(BaseLLM):
    """OpenAI LLM client with full parameter support"""

    def __init__(
            self,
            model: str = "gpt-4",
            api_key: Optional[str] = None,
            organization: Optional[str] = None,
            base_url: str | httpx.URL | None = None,
            **kwargs: Any
    ):
        super().__init__(model=model, **kwargs)
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            organization=organization or os.getenv("OPENAI_ORG_ID"),
            base_url=base_url,
        )

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=self.stop,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI generation failed: {str(e)}")

    def stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=self.stop,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise RuntimeError(f"OpenAI streaming failed: {str(e)}")

    def get_num_tokens(self, text: str) -> int:
        # Use OpenAI's tokenizer for accurate count
        encoder = tiktoken.get_encoding(self.model)
        tokens = encoder.encode(text)
        return len(tokens)
