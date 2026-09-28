from app.ai.provider import AIProvider, ExtractedIntent


class AIGateway:
    """Application boundary between AI providers and deterministic domain logic."""

    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def extract_appointment_intent(self, text: str) -> ExtractedIntent:
        return self.provider.extract_intent(text)
