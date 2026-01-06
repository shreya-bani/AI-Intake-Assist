from providers.base_provider import BaseProvider
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.azure_openai_provider import AzureOpenAIProvider
from config import settings


class ProviderFactory:
    """Factory class for creating LLM provider instances."""

    @staticmethod
    def create_provider() -> BaseProvider:
        """
        Create and return the appropriate LLM provider based on configuration.

        Returns:
            An instance of the configured LLM provider

        Raises:
            ValueError: If provider type is invalid or required API key is missing
        """
        provider_type = settings.LLM_PROVIDER.lower()
        model_name = settings.MODEL_NAME

        if provider_type == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")

            provider = OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model_name=model_name
            )
            provider.validate_config()
            return provider

        elif provider_type == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY is required when using Anthropic provider")

            provider = AnthropicProvider(
                api_key=settings.ANTHROPIC_API_KEY,
                model_name=model_name
            )
            provider.validate_config()
            return provider

        elif provider_type == "azure_openai":
            if not settings.AZURE_OPENAI_API_KEY:
                raise ValueError("AZURE_OPENAI_API_KEY is required when using Azure OpenAI provider")
            if not settings.AZURE_OPENAI_ENDPOINT:
                raise ValueError("AZURE_OPENAI_ENDPOINT is required when using Azure OpenAI provider")
            if not settings.AZURE_OPENAI_MODEL_NAME:
                raise ValueError("AZURE_OPENAI_MODEL_NAME is required when using Azure OpenAI provider")

            provider = AzureOpenAIProvider(
                api_key=settings.AZURE_OPENAI_API_KEY,
                endpoint=settings.AZURE_OPENAI_ENDPOINT,
                model_name=settings.AZURE_OPENAI_MODEL_NAME,
                api_version=settings.AZURE_OPENAI_API_VERSION
            )
            provider.validate_config()
            return provider

        else:
            raise ValueError(
                f"Invalid LLM_PROVIDER: {provider_type}. "
                f"Supported providers: openai, anthropic, azure_openai"
            )


def get_provider() -> BaseProvider:
    """
    Convenience function to get a provider instance.

    Returns:
        An instance of the configured LLM provider
    """
    return ProviderFactory.create_provider()
