"""Article Domain"""

from typing import TypedDict

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.blog.domain.events.article_created import ArticleCreated
from src.blog.domain.events.article_published import ArticlePublished
from src.blog.domain.events.article_unpublished import ArticleUnpublished
from src.blog.domain.events.article_updated import ArticleUpdated
from src.shared.domain.domain_model import DomainModel


class ArticleUpdateParams(TypedDict):
    title: str
    description: str
    content: str
    slug: str


@dataclass
class Article(DomainModel):
    """Article on blog"""

    id: str
    title: str
    description: str
    content: str
    slug: str
    author_id: str
    created_at: datetime
    updated_at: datetime
    published: bool

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        content: str,
        slug: str,
        author_id: str,
    ) -> "Article":
        """Factory method to create a new article."""
        id = str(uuid4())
        now = datetime.now()
        article = Article(
            id=id,
            title=title,
            description=description,
            content=content,
            slug=slug,
            author_id=author_id,
            created_at=now,
            updated_at=now,
            published=False,
        )
        article.record(ArticleCreated(id))
        return article

    def update(self, payload: ArticleUpdateParams) -> None:
        """Update article fields and refresh updated_at timestamp."""
        if title := payload.get("title"):
            self.title = title
        if description := payload.get("description"):
            self.description = description
        if content := payload.get("content"):
            self.content = content
        if slug := payload.get("slug"):
            self.slug = slug
        self.updated_at = datetime.now()
        self.record(ArticleUpdated(self.id, dict(payload)))

    def publish(self) -> None:
        """Publish the article."""
        self.published = True
        self.updated_at = datetime.now()
        self.record(ArticlePublished(self.id))

    def unpublish(self) -> None:
        """Unpublish the article."""
        self.published = False
        self.updated_at = datetime.now()
        self.record(ArticleUnpublished(self.id))
