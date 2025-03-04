from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional


@dataclass
class UsageStats:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_cost: float = 0.0


class BaseLLM(ABC):
    """Base class for all LLM clients with Langchain-style parameters"""

    def __init__(
            self,
            model: str,
            temperature: float = 0.7,
            max_tokens: Optional[int] = None,
            top_p: float = 1.0,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
            stop: Optional[List[str]] = None,
            **kwargs: Any
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.kwargs = kwargs
        self.usage_stats = UsageStats()
        self._cost_per_token = kwargs.get("cost_per_token", 0.0)

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from the LLM"""
        raise NotImplementedError()
        # pass

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """Stream response from the LLM"""
        raise NotImplementedError()
        # pass

    @abstractmethod
    def get_num_tokens(self, text: str) -> int:
        """Calculate number of tokens for the given text"""
        raise NotImplementedError()
        # pass

    def _update_usage(self, prompt_tokens: int, completion_tokens: int):
        self.usage_stats.prompt_tokens += prompt_tokens
        self.usage_stats.completion_tokens += completion_tokens
        self.usage_stats.total_cost += (
                (prompt_tokens + completion_tokens) * self._cost_per_token
        )
