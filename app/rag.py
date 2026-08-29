from pathlib import Path
from app.embeddings import EmbeddingClient
import math


class RAG:

    def __init__(
        self,
        documents_path: str = "documents",
        embedding_client: EmbeddingClient | None = None,
    ):
        self.documents_path = Path(documents_path)
        self.embedding_client = embedding_client or EmbeddingClient()

        self._chunks: list[str] = []
        self._embeddings: list[list[float]] = []
        self._build_index()

    def load_documents(self) -> list[str]:
        chunks = []

        for file in self.documents_path.glob("*.md"):
            content = file.read_text(encoding="utf-8")
            file_chunks = self.chunk_text(content)
            chunks.extend(file_chunks)

        return chunks

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
    ) -> list[str]:
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)

        return chunks

    # ---------------------------------------------------------
    # 2. Create embeddings for our documents
    # ---------------------------------------------------------

    def _build_index(self):
        self._chunks = self.load_documents()

        print(f"RAG: Creating embeddings for " f"{len(self._chunks)} chunks...")

        self._embeddings = [
            self.embedding_client.embed(chunk) for chunk in self._chunks
        ]
        print("RAG: Embedding index ready.")

    # ---------------------------------------------------------
    # 3. Compare two vectors
    # ---------------------------------------------------------

    def _cosine_similarity(
        self,
        a: list[float],
        b: list[float],
    ) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))

        magnitude_a = math.sqrt(sum(x * x for x in a))

        magnitude_b = math.sqrt(sum(y * y for y in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def search(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.5,
    ) -> list[str]:

        query_embedding = self.embedding_client.embed(query)
        scored_chunks = []

        for chunk, embedding in zip(
            self._chunks,
            self._embeddings,
        ):

            similarity = self._cosine_similarity(
                query_embedding,
                embedding,
            )

            print(f"RAG similarity: {similarity:.3f} " f"| {chunk[:80]}")

            if similarity >= similarity_threshold:
                scored_chunks.append((similarity, chunk))

        scored_chunks.sort(
                key=lambda item: item[0],
                reverse=True,
            )

        return [chunk for _, chunk in scored_chunks[:top_k]]
