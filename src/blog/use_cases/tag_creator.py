from src.blog.domain.errors.tag_already_exists import TagAlreadyExists
from src.blog.domain.tag import Tag
from src.blog.domain.tag_repository import TagRepository
from src.shared.use_cases.use_case import UseCase


class TagCreator(UseCase):
    def __init__(self, tag_repository: TagRepository) -> None:
        self.tag_repository = tag_repository

    def execute(self, name: str, slug: str) -> Tag:
        existing = self.tag_repository.find_by_slug(slug)
        if existing:
            raise TagAlreadyExists(f"Slug '{slug}' is already in use.")

        tag = Tag.create(name=name, slug=slug)
        self.tag_repository.save(tag)
        return tag
