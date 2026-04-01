from src.shared.domain.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError,
)


class EmbeddingServiceCohere(EmbeddingService):
    """Embedding service implementation using Cohere API."""

    def __init__(
        self,
        api_key: str,
        model: str = "embed-english-v3.0",
    ) -> None:
        """Initialize Cohere embedding service.

        Args:
            api_key: Cohere API key
            model: Model name (default: embed-english-v3.0)

        Raises:
            ImportError: If cohere library is not installed
        """
        try:
            import cohere  # type: ignore[import-not-found]
        except ImportError as e:
            raise ImportError(
                "cohere library is required for EmbeddingServiceCohere. "
                "Install it with: pip install cohere"
            ) from e

        if not api_key:
            raise ValueError("Cohere API key is required")

        self._client = cohere.ClientV2(api_key=api_key)
        self._model = model

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
            response = self._client.embed(
                model=self._model,
                texts=[text],
                input_type="search_document",
            )
            return list(response.embeddings[0])
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
            response = self._client.embed(
                model=self._model,
                texts=texts,
                input_type="search_document",
            )
            return [list(embedding) for embedding in response.embeddings]
        except Exception as e:
            raise EmbeddingServiceError(f"Failed to embed texts: {str(e)}") from e
