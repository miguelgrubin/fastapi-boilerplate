from src.shared.domain.events.domain_event import DomainEvent

ARTICLE_UNPUBLISHED_EVENT = "ArticleUnpublishedEvent"


class ArticleUnpublished(DomainEvent):
    def __init__(self, article_id: str) -> None:
        super().__init__(ARTICLE_UNPUBLISHED_EVENT)
        self.article_id = article_id
