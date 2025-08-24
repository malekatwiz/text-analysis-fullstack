import asyncio
from llm.llm_provider import LlmProvider
import numpy as np

class TextSimilarityService:
    def __init__(self):
        self.llm = LlmProvider()

    async def _generate_embedding(self, text) -> list[float]:
        return await self.llm.generate_embeddings(text)

    def _score_similarity(self, emb1, emb2):
        # e1 = np.array(emb1)
        e1 = np.asarray(emb1).squeeze()
        e2 = np.asarray(emb2).squeeze()
        cosine_similarity = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
        return cosine_similarity

    async def compute_similarity(self, list_of_texts: list[str]) -> float:
        if len(list_of_texts) < 2:
            raise ValueError("At least two texts are required for similarity computation.")

        emb1, emb2 = await asyncio.gather(
            self._generate_embedding(list_of_texts[0]),
            self._generate_embedding(list_of_texts[1]),
        )

        similarity_score = self._score_similarity(emb1, emb2)
        return similarity_score
