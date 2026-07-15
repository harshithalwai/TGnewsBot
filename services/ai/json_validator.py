import json

from pydantic import ValidationError

from services.ai.schemas import AIResponse


class JSONValidator:

    @staticmethod
    def validate(text: str) -> AIResponse:
        data = json.loads(text)
        return AIResponse.model_validate(data)