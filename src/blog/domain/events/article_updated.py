from src.shared.domain.events.domain_event import DomainEvent

ARTICLE_UPDATED_EVENT = "ArticleUpdatedEvent"


class ArticleUpdated(DomainEvent):
    def __init__(self, article_id: str, payload) -> None:
        super().__init__(ARTICLE_UPDATED_EVENT)
        self.article_id = article_id
        self.payload = payload
