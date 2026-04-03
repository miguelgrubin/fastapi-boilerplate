from src.shared.domain.services.embedding_service import EmbeddingService


class EmbeddingServiceFake(EmbeddingService):
    """Fake embedding service for testing and when embeddings are disabled."""

    def __init__(self, dimension: int = 1536) -> None:
        """Initialize fake embedding service.

        Args:
            dimension: Dimension of embedding vectors (default: 1536)
        """
        self._dimension = dimension

    def embed_text(self, text: str) -> list[float]:
        """Return a fake embedding vector.

        Args:
            text: The text to embed (not used in fake implementation).

        Returns:
            A list of floats of size _dimension.
        """
        # Generate deterministic fake embeddings based on text hash
        hash_value = hash(text)
        seed = abs(hash_value % (2**31))
        return [float((seed + i) % 256) / 256 for i in range(self._dimension)]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return fake embedding vectors.

        Args:
            texts: A list of texts to embed (not used in fake implementation).

        Returns:
            A list of embedding vectors.
        """
        return [self.embed_text(text) for text in texts]
