from ollama import chat

from services.ai.prompt_builder import PromptBuilder
from services.ai.json_validator import JSONValidator


class OllamaService:

    MODEL = "qwen3:4b"

    def generate(self, title: str, article: str, source: str):

        prompt = PromptBuilder.build(
            title=title,
            article=article,
            source=source,
        )

        response = chat(
            model=self.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.2,
            },
        )

        content = response.message.content

        return JSONValidator.validate(content)