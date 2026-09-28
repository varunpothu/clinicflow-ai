from app.ai.provider import AIProvider, BedrockAIProvider, MockAIProvider
from app.core.config import Settings


def build_ai_provider(settings: Settings) -> AIProvider:
    if settings.ai_provider.lower() == "bedrock":
        if not settings.bedrock_model_id:
            raise ValueError("BEDROCK_MODEL_ID is required when AI_PROVIDER=bedrock")
        return BedrockAIProvider(
            model_id=settings.bedrock_model_id,
            region_name=settings.aws_region,
            guardrail_identifier=settings.bedrock_guardrail_identifier,
            guardrail_version=settings.bedrock_guardrail_version,
        )
    return MockAIProvider()
