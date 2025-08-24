import httpx

class LlmProvider:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        self.model_name = "llama3.1"
        self.http_client = httpx.AsyncClient(timeout=60.0)

    async def generate_completion(self, prompt: str, response_format) -> dict:
        response = await self.http_client.post(
            url=f"{self.base_url}/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "format": response_format,
                "stream": False,
            }
        )

        response.raise_for_status()
        response_content = response.json()
        return response_content["response"]

    async def generate_embeddings(self, text: str) -> list[float]:
        response = await self.http_client.post(
            url=f"{self.base_url}/embed",
            json={
                "model": self.model_name,
                "input": text,
            }
        )
        response.raise_for_status()
        return response.json()["embeddings"]