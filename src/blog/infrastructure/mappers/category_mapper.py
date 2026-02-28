from src.blog.domain.category import Category
from src.blog.infrastructure.server.category_dtos import CategoryResponse


class CategoryMapper:
    @staticmethod
    def to_dto(category: Category) -> CategoryResponse:
        return CategoryResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            created_at=category.created_at,
        )
