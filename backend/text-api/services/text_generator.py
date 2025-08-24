import json

from llm.llm_provider import LlmProvider
from llm.prompts import PromptsFactory


class TextGeneratorService:
    def __init__(self):
        self.llm = LlmProvider()

    async def generate_text(self, prompt_id: str, data) -> dict:
        prompt_text, response_format = PromptsFactory.create_prompt(prompt_id, data)

        response = await self.llm.generate_completion(prompt_text, response_format)

        json.loads(response)
        return response