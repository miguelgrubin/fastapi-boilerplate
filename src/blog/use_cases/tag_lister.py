from typing import List

from src.blog.domain.tag import Tag
from src.blog.domain.tag_repository import TagRepository
from src.shared.use_cases.use_case import UseCase


class TagLister(UseCase):
    def __init__(self, tag_repository: TagRepository) -> None:
        self.tag_repository = tag_repository

    def execute(self) -> List[Tag]:
        return self.tag_repository.find_all()
