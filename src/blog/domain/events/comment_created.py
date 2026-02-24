from src.shared.domain.events.domain_event import DomainEvent

COMMENT_CREATED_EVENT = "CommentCreatedEvent"


class CommentCreated(DomainEvent):
    def __init__(self, comment_id: str, article_id: str) -> None:
        super().__init__(COMMENT_CREATED_EVENT)
        self.comment_id = comment_id
        self.article_id = article_id
