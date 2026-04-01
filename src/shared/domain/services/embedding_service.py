from abc import ABC, abstractmethod

EMBEDDING_SERVICE = "EmbeddingService"


class EmbeddingServiceError(Exception):
    """Exception raised when embedding service encounters an error."""

    pass


class EmbeddingService(ABC):
    """Abstract interface for embedding text to vector representations."""

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string into a vector.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.

        Raises:
            EmbeddingServiceError: If embedding generation fails.
        """
        pass

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings into vectors.

        Args:
            texts: A list of texts to embed.

        Returns:
            A list of embedding vectors (list of floats).

        Raises:
            EmbeddingServiceError: If embedding generation fails.
        """
        pass
