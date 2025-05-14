from collections.abc import Sequence
from enum import Enum

from langchain.chat_models import init_chat_model
from langchain.schema import BaseMessage
from langchain.schema.output_parser import StrOutputParser
from langchain_core.language_models.chat_models import BaseChatModel


class LLMProvider(Enum):
    """Enumeration of supported LLM providers and their models."""

    OPENAI_GPT_4O_MINI = "gpt-4o-mini"
    ANTHROPIC_CLAUDE_3_HAIKU = "claude-3-haiku-20241022"


def get_llm_completion(
    messages: Sequence[BaseMessage],
    model: LLMProvider,
) -> str:
    """Gets a string completion from the specified LLM.

    Args:
        messages: A sequence of BaseMessage objects (e.g., SystemMessage, HumanMessage).
        model: The LLMProvider enum member specifying which model to use.

    Returns:
        The LLM's response as a string.

    Raises:
        ValueError: If an unsupported model is selected (potentially by langchain_init_chat_model).
    """
    llm: BaseChatModel = init_chat_model(model=model.value)
    chain = llm | StrOutputParser()
    return chain.invoke(messages)
