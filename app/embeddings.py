import requests

from app.config import (
    EMBEDDING_URL,
    EMBEDDING_MODEL,
)


class EmbeddingClient:

    def embed(self, text: str) -> list[float]:

        response = requests.post(
            EMBEDDING_URL,
            json={
                "model": EMBEDDING_MODEL,
                "input": text,
            },
        )

        response.raise_for_status()
        data = response.json()

        return data["data"][0]["embedding"]
