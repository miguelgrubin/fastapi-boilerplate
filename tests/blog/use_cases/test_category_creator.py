from unittest.mock import patch

import pytest
from src.blog.domain.errors.category_already_exists import CategoryAlreadyExists
from src.blog.infrastructure.storage.category_repository_memory import CategoryRepositoryMemory
from src.blog.use_cases.category_creator import CategoryCreator


def _create_use_case():
    repo = CategoryRepositoryMemory()
    repo.clear()
    use_case = CategoryCreator(repo)
    return use_case, repo


def test_should_create_category():
    use_case, _ = _create_use_case()
    category = use_case.execute(name="Technology", slug="technology")

    assert category.id != ""
    assert category.name == "Technology"
    assert category.slug == "technology"
    assert category.created_at is not None


def test_should_raise_error_when_slug_already_exists():
    use_case, _ = _create_use_case()
    use_case.execute(name="Technology", slug="technology")

    with pytest.raises(CategoryAlreadyExists):
        use_case.execute(name="Tech", slug="technology")


@patch.object(CategoryRepositoryMemory, "save")
def test_should_save_on_repository(mock_save):
    use_case, _ = _create_use_case()
    use_case.execute(name="Technology", slug="technology")

    mock_save.assert_called()


def test_should_allow_different_slugs():
    use_case, _ = _create_use_case()
    cat1 = use_case.execute(name="Technology", slug="technology")
    cat2 = use_case.execute(name="Science", slug="science")

    assert cat1.id != cat2.id
    assert cat1.slug != cat2.slug
