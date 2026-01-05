from typing import List, Dict, Optional
from anthropic import AsyncAnthropic
from providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic Claude LLM provider implementation."""

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key
            model_name: Model ID (e.g., 'claude-3-sonnet-20240229', 'claude-3-opus-20240229')
        """
        super().__init__(api_key, model_name)
        self.client = AsyncAnthropic(api_key=api_key)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion using Anthropic's API.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response (defaults to 1024)

        Returns:
            Generated response text

        Raises:
            Exception: If API call fails
        """
        try:
            # Anthropic requires system messages to be separate
            system_message = None
            conversation_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    conversation_messages.append(msg)

            # Set default max_tokens if not provided (Anthropic requires this)
            if max_tokens is None:
                max_tokens = 1024

            # Make API call
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=conversation_messages
            )

            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def validate_config(self) -> bool:
        """
        Validate Anthropic configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If API key is invalid
        """
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        if not self.api_key.startswith("sk-ant-"):
            raise ValueError("Invalid Anthropic API key format")
        return True
