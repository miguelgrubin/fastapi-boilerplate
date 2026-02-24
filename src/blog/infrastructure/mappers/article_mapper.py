from src.blog.domain.article import Article
from src.blog.infrastructure.server.article_dtos import ArticleResponse


class ArticleMapper:
    @staticmethod
    def to_dto(article: Article) -> ArticleResponse:
        return ArticleResponse(
            id=article.id,
            title=article.title,
            description=article.description,
            content=article.content,
            slug=article.slug,
            author_id=article.author_id,
            published=article.published,
            category_id=article.category_id,
            tags=article.tags,
            created_at=article.created_at,
            updated_at=article.updated_at,
        )
