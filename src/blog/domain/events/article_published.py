from src.shared.domain.events.domain_event import DomainEvent

ARTICLE_PUBLISHED_EVENT = "ArticlePublishedEvent"


class ArticlePublished(DomainEvent):
    def __init__(self, article_id: str) -> None:
        super().__init__(ARTICLE_PUBLISHED_EVENT)
        self.article_id = article_id
