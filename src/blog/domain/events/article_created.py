from src.shared.domain.events.domain_event import DomainEvent

ARTICLE_CREATED_EVENT = "ArticleCreatedEvent"


class ArticleCreated(DomainEvent):
    def __init__(self, article_id: str) -> None:
        super().__init__(ARTICLE_CREATED_EVENT)
        self.article_id = article_id
