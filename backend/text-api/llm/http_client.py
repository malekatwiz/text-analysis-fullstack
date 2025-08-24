import httpx

class LlmHttpClient:
    def __init__(self, base_url: str, api_key: str = None, concurrency: int = 10):
        self.base_url = base_url
        self.api_key = api_key
        self.concurrency = concurrency
        self.operations = {
            "generate": "/generate",
        }

        self.client = self._create_client()

    def _create_client(self) -> httpx.AsyncClient:
        request_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.api_key:
            request_headers["api-key"] = self.api_key

        return httpx.AsyncClient(
            headers=request_headers,
            limits=httpx.Limits(max_connections=self.concurrency, max_keepalive_connections=self.concurrency),
            timeout=httpx.Timeout(10.0, connect=5.0),
        )

    async def _post(self, endpoint: str, data: dict = None) -> dict:
        response = await self.client.post(url=f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    async def generate(self, prompt, model: str, response_json_schema: dict = None):
        """
        Generate text using the specified model and prompt.
        """
        data = {
            "model": model,
            "prompt": prompt
        }

        if response_json_schema:
            data["format"] = response_json_schema

        endpoint = self.operations["generate"]
        return await self._post(endpoint=endpoint, data=data)