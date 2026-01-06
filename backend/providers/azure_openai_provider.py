from typing import List, Dict, Optional
from openai import AsyncAzureOpenAI
from providers.base_provider import BaseProvider


class AzureOpenAIProvider(BaseProvider):
    """Azure OpenAI LLM provider implementation."""

    def __init__(self, api_key: str, endpoint: str, model_name: str, api_version: str = "2024-12-01-preview"):
        """
        Initialize Azure OpenAI provider.

        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            model_name: Deployment name (e.g., 'gpt-4o', 'gpt-4')
            api_version: API version string
        """
        super().__init__(api_key, model_name)
        self.endpoint = endpoint
        self.api_version = api_version
        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion using Azure OpenAI's API.

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
            raise Exception(f"Azure OpenAI API error: {str(e)}")

    def validate_config(self) -> bool:
        """
        Validate Azure OpenAI configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.api_key:
            raise ValueError("Azure OpenAI API key is required")
        if not self.endpoint:
            raise ValueError("Azure OpenAI endpoint is required")
        if not self.model_name:
            raise ValueError("Azure OpenAI deployment name (model) is required")
        return True
