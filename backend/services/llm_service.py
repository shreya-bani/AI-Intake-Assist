from typing import List, Dict
from providers.provider_factory import get_provider
from providers.base_provider import BaseProvider


class LLMService:
    """High-level service for LLM interactions."""

    def __init__(self):
        """Initialize the LLM service with the configured provider."""
        self.provider: BaseProvider = get_provider()

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of conversation messages
            temperature: Sampling temperature

        Returns:
            Generated response text

        Raises:
            Exception: If LLM call fails
        """
        try:
            response = await self.provider.chat_completion(
                messages=messages,
                temperature=temperature
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")

    async def extract_structured_data(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Extract structured data from conversation using LLM.
        Uses lower temperature for more consistent output.

        Args:
            messages: List of conversation messages including extraction prompt

        Returns:
            Generated JSON string

        Raises:
            Exception: If LLM call fails
        """
        try:
            response = await self.provider.chat_completion(
                messages=messages,
                temperature=0.3  # Lower temperature for structured output
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to extract data: {str(e)}")


# Create a singleton instance
llm_service = LLMService()


def get_llm_service() -> LLMService:
    """Get the LLM service instance."""
    return llm_service
