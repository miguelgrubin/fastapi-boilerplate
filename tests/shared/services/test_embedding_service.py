"""Tests for embedding service implementations."""

import pytest
from src.shared.domain.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError,
)
from src.shared.infrastructure.services.embedding_service_factory import (
    create_embedding_service,
)
from src.shared.infrastructure.services.embedding_service_fake import (
    EmbeddingServiceFake,
)


class TestEmbeddingServiceFake:
    """Tests for fake embedding service."""

    def test_embed_text_returns_vector(self) -> None:
        """Test that embed_text returns a vector of correct dimension."""
        service = EmbeddingServiceFake(dimension=1536)
        vector = service.embed_text("hello world")

        assert isinstance(vector, list)
        assert len(vector) == 1536
        assert all(isinstance(v, float) for v in vector)
        assert all(0 <= v <= 1 for v in vector)

    def test_embed_text_deterministic(self) -> None:
        """Test that same text produces same embedding."""
        service = EmbeddingServiceFake(dimension=1536)
        text = "test text"

        vector1 = service.embed_text(text)
        vector2 = service.embed_text(text)

        assert vector1 == vector2

    def test_embed_text_different_for_different_texts(self) -> None:
        """Test that different texts produce different embeddings."""
        service = EmbeddingServiceFake(dimension=1536)

        vector1 = service.embed_text("hello")
        vector2 = service.embed_text("world")

        assert vector1 != vector2

    def test_embed_texts_returns_list_of_vectors(self) -> None:
        """Test that embed_texts returns correct number of vectors."""
        service = EmbeddingServiceFake(dimension=512)
        texts = ["text 1", "text 2", "text 3"]

        vectors = service.embed_texts(texts)

        assert isinstance(vectors, list)
        assert len(vectors) == 3
        assert all(isinstance(v, list) for v in vectors)
        assert all(len(v) == 512 for v in vectors)

    def test_embed_texts_empty_list(self) -> None:
        """Test that embed_texts handles empty list."""
        service = EmbeddingServiceFake()
        vectors = service.embed_texts([])

        assert vectors == []

    def test_custom_dimension(self) -> None:
        """Test that custom dimension is respected."""
        for dimension in [128, 256, 512, 1536]:
            service = EmbeddingServiceFake(dimension=dimension)
            vector = service.embed_text("test")

            assert len(vector) == dimension


class TestEmbeddingServiceFactory:
    """Tests for embedding service factory."""

    def test_creates_fake_service_when_disabled(self) -> None:
        """Test that factory creates fake service when disabled."""
        service = create_embedding_service(enabled=False)

        assert isinstance(service, EmbeddingServiceFake)

    def test_creates_fake_service_by_default(self) -> None:
        """Test that factory creates fake service by default."""
        service = create_embedding_service()

        assert isinstance(service, EmbeddingServiceFake)

    def test_raises_error_when_enabled_without_api_key(self) -> None:
        """Test that factory raises error when enabled without API key."""
        with pytest.raises(ValueError, match="COHERE_API_KEY is required"):
            create_embedding_service(enabled=True, api_key="")

    def test_respects_custom_dimension(self) -> None:
        """Test that factory respects custom dimension."""
        service = create_embedding_service(enabled=False, dimension=512)

        vector = service.embed_text("test")
        assert len(vector) == 512

    def test_creates_cohere_service_when_enabled_with_api_key(self) -> None:
        """Test that factory creates Cohere service when enabled with API key."""
        # This test will fail if cohere library is not installed,
        # but that's expected behavior
        try:
            service = create_embedding_service(enabled=True, api_key="test-key-12345")
            # Check that it's the Cohere implementation
            assert hasattr(service, "_client")
        except ImportError:
            pytest.skip("cohere library not installed")


class TestEmbeddingServiceInterface:
    """Tests to verify EmbeddingService interface compliance."""

    def test_fake_service_implements_interface(self) -> None:
        """Test that fake service implements EmbeddingService interface."""
        service = EmbeddingServiceFake()

        assert isinstance(service, EmbeddingService)
        assert hasattr(service, "embed_text")
        assert hasattr(service, "embed_texts")
        assert callable(service.embed_text)
        assert callable(service.embed_texts)
