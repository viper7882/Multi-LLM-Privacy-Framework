import ollama
from typing import Any, Generator
from ..base import BaseLLM


class OllamaClient(BaseLLM):
    """Ollama LLM client with full parameter support"""

    def __init__(
            self,
            model: str = "llama3.2",
            base_url: str = "http://localhost:11434",
            **kwargs: Any
    ):
        super().__init__(model=model, **kwargs)
        self.client = ollama.Client(host=base_url)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "max_tokens": self.max_tokens,
                    "stop": self.stop,
                },
            )
            self._update_usage(
                self.get_num_tokens(prompt),
                self.get_num_tokens(response["response"])
            )
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")

    def stream(self, prompt: str) -> Generator[str, None, None]:
        # Implement streaming with usage tracking
        total_response = []
        try:
            stream = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "max_tokens": self.max_tokens,
                    "stop": self.stop,
                },
            )

            for chunk in stream:
                total_response.append(chunk["response"])
                yield chunk["response"]

            self._update_usage(
                self.get_num_tokens(prompt),
                self.get_num_tokens("".join(total_response))
            )
        except Exception as e:
            raise RuntimeError(f"Ollama streaming failed: {str(e)}")

    def get_num_tokens(self, text: str) -> int:
        # Simplified token counting for demonstration
        return len(text.split())
