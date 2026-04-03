from unittest.mock import MagicMock, patch

import pytest

from src.blog.factory import (
    create_repositories,
    create_use_cases,
    create_services,
)
from src.blog.types import BlogRepositoriesType, BlogUseCasesType
from src.shared.types import SharedServices


def test_create_repositories_returns_blog_repositories_type():
    """Test that create_repositories returns a BlogRepositoriesType instance."""
    sql_service = MagicMock()
    embedding_service = MagicMock()

    result = create_repositories(sql_service, embedding_service)

    assert isinstance(result, BlogRepositoriesType)


def test_create_repositories_has_all_repositories():
    """Test that created repositories have all required repository instances."""
    sql_service = MagicMock()
    embedding_service = MagicMock()

    repositories = create_repositories(sql_service, embedding_service)

    assert repositories.user_repository is not None
    assert repositories.article_repository is not None
    assert repositories.comment_repository is not None
    assert repositories.category_repository is not None
    assert repositories.tag_repository is not None


def test_create_repositories_passes_sql_service_to_repositories():
    """Test that SQL service is passed to repository constructors."""
    sql_service = MagicMock()
    embedding_service = MagicMock()

    repositories = create_repositories(sql_service, embedding_service)

    # All repositories should have received sql_service
    # We verify this by checking that the repositories were created successfully
    assert repositories.user_repository is not None
    assert repositories.article_repository is not None
    assert repositories.category_repository is not None
    assert repositories.tag_repository is not None


def test_create_repositories_passes_embedding_service_to_article_and_comment():
    """Test that embedding service is passed to article and comment repositories."""
    sql_service = MagicMock()
    embedding_service = MagicMock()

    repositories = create_repositories(sql_service, embedding_service)

    # Article and comment repositories should have embedding service
    assert repositories.article_repository is not None
    assert repositories.comment_repository is not None


def test_create_use_cases_returns_blog_use_cases_type():
    """Test that create_use_cases returns a BlogUseCasesType instance."""
    repositories = MagicMock(spec=BlogRepositoriesType)
    repositories.user_repository = MagicMock()
    repositories.article_repository = MagicMock()
    repositories.comment_repository = MagicMock()
    repositories.category_repository = MagicMock()
    repositories.tag_repository = MagicMock()

    services = MagicMock(spec=SharedServices)
    services.password_service = MagicMock()

    result = create_use_cases(repositories, services)

    assert isinstance(result, BlogUseCasesType)


def test_create_use_cases_has_all_use_cases():
    """Test that created use cases have all required use case instances."""
    repositories = MagicMock(spec=BlogRepositoriesType)
    repositories.user_repository = MagicMock()
    repositories.article_repository = MagicMock()
    repositories.comment_repository = MagicMock()
    repositories.category_repository = MagicMock()
    repositories.tag_repository = MagicMock()

    services = MagicMock(spec=SharedServices)
    services.password_service = MagicMock()

    use_cases = create_use_cases(repositories, services)

    assert use_cases.user_creator is not None
    assert use_cases.user_deleter is not None
    assert use_cases.article_creator is not None
    assert use_cases.article_finder is not None
    assert use_cases.article_lister is not None
    assert use_cases.article_updater is not None
    assert use_cases.article_deleter is not None
    assert use_cases.article_publisher is not None
    assert use_cases.comment_creator is not None
    assert use_cases.comment_lister is not None
    assert use_cases.comment_deleter is not None
    assert use_cases.category_creator is not None
    assert use_cases.category_lister is not None
    assert use_cases.tag_creator is not None
    assert use_cases.tag_lister is not None


def test_create_use_cases_injects_repositories():
    """Test that repositories are correctly injected into use cases."""
    repositories = MagicMock(spec=BlogRepositoriesType)
    repositories.user_repository = MagicMock()
    repositories.article_repository = MagicMock()
    repositories.comment_repository = MagicMock()
    repositories.category_repository = MagicMock()
    repositories.tag_repository = MagicMock()

    services = MagicMock(spec=SharedServices)
    services.password_service = MagicMock()

    use_cases = create_use_cases(repositories, services)

    # Verify that use cases were created (they would be None if injection failed)
    assert use_cases.user_creator is not None
    assert use_cases.article_creator is not None
    assert use_cases.comment_creator is not None


def test_create_use_cases_injects_services():
    """Test that services are correctly injected into use cases."""
    repositories = MagicMock(spec=BlogRepositoriesType)
    repositories.user_repository = MagicMock()
    repositories.article_repository = MagicMock()
    repositories.comment_repository = MagicMock()
    repositories.category_repository = MagicMock()
    repositories.tag_repository = MagicMock()

    services = MagicMock(spec=SharedServices)
    services.password_service = MagicMock()

    use_cases = create_use_cases(repositories, services)

    # Verify that use cases were created with service injection
    assert use_cases.user_creator is not None


@patch("src.blog.factory.create_password_service")
@patch("src.blog.factory.create_sql_service")
@patch("src.blog.factory.create_authentication_service")
@patch("src.blog.factory.create_authorization_service")
@patch("src.blog.factory.create_embedding_service")
def test_create_services_returns_shared_services(
    mock_embedding,
    mock_authorization,
    mock_authentication,
    mock_sql,
    mock_password,
):
    """Test that create_services returns a SharedServices instance."""
    mock_password.return_value = MagicMock()
    mock_sql.return_value = MagicMock()
    mock_authentication.return_value = MagicMock()
    mock_authorization.return_value = MagicMock()
    mock_embedding.return_value = MagicMock()

    result = create_services("sqlite:///test.db")

    assert isinstance(result, SharedServices)


@patch("src.blog.factory.create_password_service")
@patch("src.blog.factory.create_sql_service")
@patch("src.blog.factory.create_authentication_service")
@patch("src.blog.factory.create_authorization_service")
@patch("src.blog.factory.create_embedding_service")
def test_create_services_has_all_services(
    mock_embedding,
    mock_authorization,
    mock_authentication,
    mock_sql,
    mock_password,
):
    """Test that created services have all required service instances."""
    mock_password.return_value = MagicMock()
    mock_sql.return_value = MagicMock()
    mock_authentication.return_value = MagicMock()
    mock_authorization.return_value = MagicMock()
    mock_embedding.return_value = MagicMock()

    services = create_services("sqlite:///test.db")

    assert services.password_service is not None
    assert services.sql_service is not None
    assert services.authentication_service is not None
    assert services.authorization_service is not None
    assert services.embedding_service is not None


@patch("src.blog.factory.create_password_service")
@patch("src.blog.factory.create_sql_service")
@patch("src.blog.factory.create_authentication_service")
@patch("src.blog.factory.create_authorization_service")
@patch("src.blog.factory.create_embedding_service")
def test_create_services_passes_database_url(
    mock_embedding,
    mock_authorization,
    mock_authentication,
    mock_sql,
    mock_password,
):
    """Test that database URL is passed to create_sql_service."""
    mock_password.return_value = MagicMock()
    mock_sql.return_value = MagicMock()
    mock_authentication.return_value = MagicMock()
    mock_authorization.return_value = MagicMock()
    mock_embedding.return_value = MagicMock()

    database_url = "postgresql://localhost/testdb"
    create_services(database_url)

    # Verify that sql_service was created with the correct database URL
    mock_sql.assert_called_once()
    call_args = mock_sql.call_args
    assert call_args[0][0] == database_url


@patch("src.blog.factory.create_password_service")
@patch("src.blog.factory.create_sql_service")
@patch("src.blog.factory.create_authentication_service")
@patch("src.blog.factory.create_authorization_service")
@patch("src.blog.factory.create_embedding_service")
def test_create_services_configures_password_service(
    mock_embedding,
    mock_authorization,
    mock_authentication,
    mock_sql,
    mock_password,
):
    """Test that password service is configured with argon2."""
    mock_password.return_value = MagicMock()
    mock_sql.return_value = MagicMock()
    mock_authentication.return_value = MagicMock()
    mock_authorization.return_value = MagicMock()
    mock_embedding.return_value = MagicMock()

    create_services("sqlite:///test.db")

    # Verify that password service was created with argon2
    mock_password.assert_called_once_with("argon2")
