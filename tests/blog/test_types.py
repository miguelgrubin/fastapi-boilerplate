from unittest.mock import MagicMock

import pytest

from src.blog.types import BlogRepositoriesType, BlogUseCasesType


def test_blog_repositories_type_instantiation():
    """Test that BlogRepositoriesType can be instantiated with all repositories."""
    user_repo = MagicMock()
    article_repo = MagicMock()
    comment_repo = MagicMock()
    category_repo = MagicMock()
    tag_repo = MagicMock()

    repositories = BlogRepositoriesType(
        user_repository=user_repo,
        article_repository=article_repo,
        comment_repository=comment_repo,
        category_repository=category_repo,
        tag_repository=tag_repo,
    )

    assert repositories.user_repository == user_repo
    assert repositories.article_repository == article_repo
    assert repositories.comment_repository == comment_repo
    assert repositories.category_repository == category_repo
    assert repositories.tag_repository == tag_repo


def test_blog_repositories_type_has_all_attributes():
    """Test that BlogRepositoriesType has all required repository attributes."""
    repos = BlogRepositoriesType(
        user_repository=MagicMock(),
        article_repository=MagicMock(),
        comment_repository=MagicMock(),
        category_repository=MagicMock(),
        tag_repository=MagicMock(),
    )

    assert hasattr(repos, "user_repository")
    assert hasattr(repos, "article_repository")
    assert hasattr(repos, "comment_repository")
    assert hasattr(repos, "category_repository")
    assert hasattr(repos, "tag_repository")


def test_blog_use_cases_type_instantiation():
    """Test that BlogUseCasesType can be instantiated with all use cases."""
    user_creator = MagicMock()
    user_deleter = MagicMock()
    article_creator = MagicMock()
    article_finder = MagicMock()
    article_lister = MagicMock()
    article_updater = MagicMock()
    article_deleter = MagicMock()
    article_publisher = MagicMock()
    comment_creator = MagicMock()
    comment_lister = MagicMock()
    comment_deleter = MagicMock()
    category_creator = MagicMock()
    category_lister = MagicMock()
    tag_creator = MagicMock()
    tag_lister = MagicMock()

    use_cases = BlogUseCasesType(
        user_creator=user_creator,
        user_deleter=user_deleter,
        article_creator=article_creator,
        article_finder=article_finder,
        article_lister=article_lister,
        article_updater=article_updater,
        article_deleter=article_deleter,
        article_publisher=article_publisher,
        comment_creator=comment_creator,
        comment_lister=comment_lister,
        comment_deleter=comment_deleter,
        category_creator=category_creator,
        category_lister=category_lister,
        tag_creator=tag_creator,
        tag_lister=tag_lister,
    )

    assert use_cases.user_creator == user_creator
    assert use_cases.user_deleter == user_deleter
    assert use_cases.article_creator == article_creator
    assert use_cases.article_finder == article_finder
    assert use_cases.article_lister == article_lister
    assert use_cases.article_updater == article_updater
    assert use_cases.article_deleter == article_deleter
    assert use_cases.article_publisher == article_publisher
    assert use_cases.comment_creator == comment_creator
    assert use_cases.comment_lister == comment_lister
    assert use_cases.comment_deleter == comment_deleter
    assert use_cases.category_creator == category_creator
    assert use_cases.category_lister == category_lister
    assert use_cases.tag_creator == tag_creator
    assert use_cases.tag_lister == tag_lister


def test_blog_use_cases_type_has_all_attributes():
    """Test that BlogUseCasesType has all required use case attributes."""
    use_cases = BlogUseCasesType(
        user_creator=MagicMock(),
        user_deleter=MagicMock(),
        article_creator=MagicMock(),
        article_finder=MagicMock(),
        article_lister=MagicMock(),
        article_updater=MagicMock(),
        article_deleter=MagicMock(),
        article_publisher=MagicMock(),
        comment_creator=MagicMock(),
        comment_lister=MagicMock(),
        comment_deleter=MagicMock(),
        category_creator=MagicMock(),
        category_lister=MagicMock(),
        tag_creator=MagicMock(),
        tag_lister=MagicMock(),
    )

    assert hasattr(use_cases, "user_creator")
    assert hasattr(use_cases, "user_deleter")
    assert hasattr(use_cases, "article_creator")
    assert hasattr(use_cases, "article_finder")
    assert hasattr(use_cases, "article_lister")
    assert hasattr(use_cases, "article_updater")
    assert hasattr(use_cases, "article_deleter")
    assert hasattr(use_cases, "article_publisher")
    assert hasattr(use_cases, "comment_creator")
    assert hasattr(use_cases, "comment_lister")
    assert hasattr(use_cases, "comment_deleter")
    assert hasattr(use_cases, "category_creator")
    assert hasattr(use_cases, "category_lister")
    assert hasattr(use_cases, "tag_creator")
    assert hasattr(use_cases, "tag_lister")
