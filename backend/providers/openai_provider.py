from typing import List, Dict, Optional
from openai import AsyncOpenAI
from providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model_name: Model ID (e.g., 'gpt-4-turbo-preview', 'gpt-3.5-turbo')
        """
        super().__init__(api_key, model_name)
        self.client = AsyncOpenAI(api_key=api_key)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion using OpenAI's API.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Generated response text

        Raises:
            Exception: If API call fails
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def validate_config(self) -> bool:
        """
        Validate OpenAI configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If API key is invalid
        """
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        if not self.api_key.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        return True
