from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseProvider(ABC):
    """
    Abstract base class for LLM providers.
    All LLM provider implementations must inherit from this class and implement its methods.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize the provider with API credentials and model configuration.

        Args:
            api_key: API key for the LLM service
            model_name: Name/ID of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     Format: [{"role": "system"|"user"|"assistant", "content": "..."}]
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response (None for default)

        Returns:
            The generated response text

        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate that the provider configuration is correct and API key is valid.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        pass

    def format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format messages to match the provider's expected format.
        Default implementation returns messages as-is.
        Override this method if your provider requires special formatting.

        Args:
            messages: List of message dicts

        Returns:
            Formatted messages
        """
        return messages
