from src.blog.infrastructure.storage.tag_repository_memory import TagRepositoryMemory
from src.blog.use_cases.tag_creator import TagCreator
from src.blog.use_cases.tag_lister import TagLister


def _create_repositories():
    repo = TagRepositoryMemory()
    repo.clear()
    return repo


def test_should_return_empty_list_when_no_tags():
    repo = _create_repositories()
    lister = TagLister(repo)

    tags = lister.execute()

    assert tags == []


def test_should_return_all_tags():
    repo = _create_repositories()
    creator = TagCreator(repo)
    creator.execute(name="Python", slug="python")
    creator.execute(name="JavaScript", slug="javascript")
    creator.execute(name="Rust", slug="rust")

    lister = TagLister(repo)
    tags = lister.execute()

    assert len(tags) == 3


def test_should_return_tags_with_correct_data():
    repo = _create_repositories()
    creator = TagCreator(repo)
    creator.execute(name="Python", slug="python")

    lister = TagLister(repo)
    tags = lister.execute()

    assert len(tags) == 1
    assert tags[0].name == "Python"
    assert tags[0].slug == "python"
