"""Factory functions for embedding service creation."""

from src.shared.domain.services.embedding_service import EmbeddingService
from src.shared.infrastructure.services.embedding_service_cohere import (
    EmbeddingServiceCohere,
)
from src.shared.infrastructure.services.embedding_service_fake import (
    EmbeddingServiceFake,
)


def create_embedding_service(
    enabled: bool = False,
    api_key: str = "",
    model: str = "embed-english-v3.0",
    dimension: int = 1536,
) -> EmbeddingService:
    """Create an embedding service based on configuration.

    Args:
        enabled: Whether to enable embeddings. If False, returns fake service.
        api_key: Cohere API key (required if enabled=True).
        model: Cohere model name.
        dimension: Embedding vector dimension.

    Returns:
        An EmbeddingService implementation.

    Raises:
        ValueError: If enabled=True but api_key is empty.
    """
    if not enabled:
        return EmbeddingServiceFake(dimension=dimension)

    if not api_key:
        raise ValueError("COHERE_API_KEY is required when EMBEDDINGS_ENABLED=True")

    return EmbeddingServiceCohere(api_key=api_key, model=model)
