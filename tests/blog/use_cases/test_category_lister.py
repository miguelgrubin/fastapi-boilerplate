from src.blog.infrastructure.storage.category_repository_memory import CategoryRepositoryMemory
from src.blog.use_cases.category_creator import CategoryCreator
from src.blog.use_cases.category_lister import CategoryLister


def _create_repositories():
    repo = CategoryRepositoryMemory()
    repo.clear()
    return repo


def test_should_return_empty_list_when_no_categories():
    repo = _create_repositories()
    lister = CategoryLister(repo)

    categories = lister.execute()

    assert categories == []


def test_should_return_all_categories():
    repo = _create_repositories()
    creator = CategoryCreator(repo)
    creator.execute(name="Technology", slug="technology")
    creator.execute(name="Science", slug="science")
    creator.execute(name="Sports", slug="sports")

    lister = CategoryLister(repo)
    categories = lister.execute()

    assert len(categories) == 3


def test_should_return_categories_with_correct_data():
    repo = _create_repositories()
    creator = CategoryCreator(repo)
    creator.execute(name="Technology", slug="technology")

    lister = CategoryLister(repo)
    categories = lister.execute()

    assert len(categories) == 1
    assert categories[0].name == "Technology"
    assert categories[0].slug == "technology"
