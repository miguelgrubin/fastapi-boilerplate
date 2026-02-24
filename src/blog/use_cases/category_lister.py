from typing import List

from src.blog.domain.category import Category
from src.blog.domain.category_repository import CategoryRepository
from src.shared.use_cases.use_case import UseCase


class CategoryLister(UseCase):
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.find_all()
