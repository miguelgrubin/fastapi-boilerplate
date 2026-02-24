from src.blog.domain.category import Category
from src.blog.domain.category_repository import CategoryRepository
from src.blog.domain.errors.category_already_exists import CategoryAlreadyExists
from src.shared.use_cases.use_case import UseCase


class CategoryCreator(UseCase):
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    def execute(self, name: str, slug: str) -> Category:
        existing = self.category_repository.find_by_slug(slug)
        if existing:
            raise CategoryAlreadyExists(f"Slug '{slug}' is already in use.")

        category = Category.create(name=name, slug=slug)
        self.category_repository.save(category)
        return category
