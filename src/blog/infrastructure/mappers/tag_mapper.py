from src.blog.domain.tag import Tag
from src.blog.infrastructure.server.tag_dtos import TagResponse


class TagMapper:
    @staticmethod
    def to_dto(tag: Tag) -> TagResponse:
        return TagResponse(
            id=tag.id,
            name=tag.name,
            slug=tag.slug,
            created_at=tag.created_at,
        )
