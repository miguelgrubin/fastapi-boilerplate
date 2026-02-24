from unittest.mock import patch

import pytest
from src.blog.domain.errors.tag_already_exists import TagAlreadyExists
from src.blog.infrastructure.storage.tag_repository_memory import TagRepositoryMemory
from src.blog.use_cases.tag_creator import TagCreator


def _create_use_case():
    repo = TagRepositoryMemory()
    repo.clear()
    use_case = TagCreator(repo)
    return use_case, repo


def test_should_create_tag():
    use_case, _ = _create_use_case()
    tag = use_case.execute(name="Python", slug="python")

    assert tag.id != ""
    assert tag.name == "Python"
    assert tag.slug == "python"
    assert tag.created_at is not None


def test_should_raise_error_when_slug_already_exists():
    use_case, _ = _create_use_case()
    use_case.execute(name="Python", slug="python")

    with pytest.raises(TagAlreadyExists):
        use_case.execute(name="Python Language", slug="python")


@patch.object(TagRepositoryMemory, "save")
def test_should_save_on_repository(mock_save):
    use_case, _ = _create_use_case()
    use_case.execute(name="Python", slug="python")

    mock_save.assert_called()


def test_should_allow_different_slugs():
    use_case, _ = _create_use_case()
    tag1 = use_case.execute(name="Python", slug="python")
    tag2 = use_case.execute(name="JavaScript", slug="javascript")

    assert tag1.id != tag2.id
    assert tag1.slug != tag2.slug
