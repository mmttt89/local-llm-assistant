from pathlib import Path
from app.embeddings import EmbeddingClient
import math
import json


class RAG:

    def __init__(
        self,
        documents_path: str = "documents",
        embedding_client: EmbeddingClient | None = None,
    ):
        self.documents_path = Path(documents_path)
        self.embedding_client = embedding_client or EmbeddingClient()

        self._chunks: list[dict] = []
        self._embeddings: list[list[float]] = []
        self._build_index()

    INDEX_PATH = Path("data/rag_index.json")

    def load_documents(self) -> list[dict]:
        chunks = []

        for file in self.documents_path.glob("*.md"):
            content = file.read_text(encoding="utf-8")
            file_chunks = self.chunk_text(content)

            for chunk in file_chunks:
                chunks.append(
                    {
                        "text": chunk["text"],
                        "source": file.name,
                        "section": chunk["section"],
                    }
                )

        return chunks

    def _document_timestamps(self) -> dict[str, float]:
        return {
            file.name: file.stat().st_mtime for file in self.documents_path.glob("*.md")
        }

    def chunk_text(self, text: str) -> list[dict]:
        sections = []
        current_section = []
        current_title = "Document"

        for line in text.splitlines():
            if line.startswith("#"):
                if current_section:
                    sections.append(
                        {
                            "text": "\n".join(current_section).strip(),
                            "section": current_title,
                        }
                    )
                    current_section = []

                current_title = line.lstrip("#").strip()

            current_section.append(line)

        if current_section:
            sections.append(
                {
                    "text": "\n".join(current_section).strip(),
                    "section": current_title,
                }
            )

        return [section for section in sections if section["text"]]

    # Create embeddings for our documents
    def _build_index(self):
        current_timestamps = self._document_timestamps()

        if self.INDEX_PATH.exists():
            print("RAG: Loading existing embedding index...")

            try:
                data = json.loads(self.INDEX_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                print("RAG: Existing index is invalid. " "Rebuilding index...")
                data = None

            if data is not None:
                saved_timestamps = data.get("documents", {})

                if saved_timestamps == current_timestamps:
                    chunks = data.get("chunks", [])

                    index_has_sections = all(
                        isinstance(chunk, dict) and "section" in chunk
                        for chunk in chunks
                    )

                    if index_has_sections:
                        self._chunks = chunks
                        self._embeddings = data["embeddings"]

                        print(
                            f"RAG: Loaded {len(self._chunks)} chunks "
                            "from index."
                        )
                        return

                    print(
                        "RAG: Existing index has outdated chunk metadata. "
                        "Rebuilding index..."
                    )

        self._chunks = self.load_documents()

        print(f"RAG: Creating embeddings for " f"{len(self._chunks)} chunks...")

        self._embeddings = [
            self.embedding_client.embed(chunk["text"]) for chunk in self._chunks
        ]

        self.INDEX_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.INDEX_PATH.write_text(
            json.dumps(
                {
                    "documents": current_timestamps,
                    "chunks": self._chunks,
                    "embeddings": self._embeddings,
                }
            ),
            encoding="utf-8",
        )

        print("RAG: Embedding index saved.")

    # Compare two vectors
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
    ) -> list[dict]:
        query_embedding = self.embedding_client.embed(query)
        scored_chunks = []

        for chunk, embedding in zip(self._chunks, self._embeddings):
            similarity = self._cosine_similarity(query_embedding, embedding)

            print(
                f"RAG similarity: {similarity:.3f} "
                f"| {chunk['source']} "
                f"| {chunk['section']} "
                f"| {chunk['text'][:80]}"
            )

            if similarity >= similarity_threshold:
                scored_chunks.append((similarity, chunk))

        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            {
                "score": similarity,
                **chunk,
            }
            for similarity, chunk in scored_chunks[:top_k]
        ]
