from collections.abc import Sequence
from enum import Enum

from langchain.schema import BaseMessage

class LLMProvider(Enum):
    """Enumeration of supported LLM providers and their models."""

    OPENAI_GPT_4O_MINI: LLMProvider
    ANTHROPIC_CLAUDE_3_HAIKU: LLMProvider

def get_llm_completion(
    messages: Sequence[BaseMessage],
    model: LLMProvider,
) -> str: ...
