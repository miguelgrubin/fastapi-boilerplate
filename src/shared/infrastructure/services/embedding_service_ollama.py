from langchain_ollama import OllamaEmbeddings
from src.shared.domain.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError,
)


class EmbeddingServiceOllama(EmbeddingService):
    """Embedding service implementation using Cohere API."""

    def __init__(
        self,
        model: str = "llama3",
    ) -> None:
        """Initialize Cohere embedding service.

        Args:
            model: Model name (default: llama3)

        """

        self._model = model
        self._embeddings = OllamaEmbeddings(model=model)

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.

        Raises:
            EmbeddingServiceError: If embedding generation fails.
        """
        try:
            return self._embeddings.embed_query(text)
        except Exception as e:
            raise EmbeddingServiceError(f"Failed to embed text: {str(e)}") from e

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings.

        Args:
            texts: A list of texts to embed.

        Returns:
            A list of embedding vectors (list of floats).

        Raises:
            EmbeddingServiceError: If embedding generation fails.
        """
        if not texts:
            return []

        try:
            return self._embeddings.embed_documents(texts)
        except Exception as e:
            raise EmbeddingServiceError(f"Failed to embed texts: {str(e)}") from e
