from src.blog.domain.comment import Comment
from src.blog.domain.events.comment_created import COMMENT_CREATED_EVENT, CommentCreated
from src.blog.domain.events.comment_deleted import COMMENT_DELETED_EVENT, CommentDeleted


def _create_comment(**overrides):
    defaults = {
        "content": "Great article!",
        "author_id": "author-456",
        "article_id": "article-789",
    }
    defaults.update(overrides)
    return Comment.create(**defaults)


def test_should_create_comment_with_valid_fields():
    comment = _create_comment()
    assert comment.id != ""
    assert comment.content == "Great article!"
    assert comment.author_id == "author-456"
    assert comment.article_id == "article-789"
    assert comment.created_at is not None
    assert comment.updated_at is not None


def test_should_record_comment_created_event():
    comment = _create_comment()
    events = comment.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], CommentCreated)
    assert events[0].comment_id == comment.id
    assert events[0].article_id == "article-789"
    assert events[0].event_type == COMMENT_CREATED_EVENT


def test_should_mark_deleted():
    comment = _create_comment()
    comment.pull_domain_events()
    comment.mark_deleted()
    events = comment.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], CommentDeleted)
    assert events[0].event_type == COMMENT_DELETED_EVENT


def test_should_record_comment_deleted_event_with_article_id():
    comment = _create_comment(article_id="art-specific")
    comment.pull_domain_events()
    comment.mark_deleted()
    events = comment.pull_domain_events()
    assert events[0].comment_id == comment.id
    assert events[0].article_id == "art-specific"
