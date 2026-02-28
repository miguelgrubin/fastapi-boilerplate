from src.blog.domain.article import Article
from src.blog.domain.events.article_created import ARTICLE_CREATED_EVENT, ArticleCreated
from src.blog.domain.events.article_published import ARTICLE_PUBLISHED_EVENT, ArticlePublished
from src.blog.domain.events.article_unpublished import (
    ARTICLE_UNPUBLISHED_EVENT,
    ArticleUnpublished,
)
from src.blog.domain.events.article_updated import ARTICLE_UPDATED_EVENT, ArticleUpdated


def _create_article(**overrides):
    defaults = {
        "title": "My First Article",
        "description": "A short description",
        "content": "Full article content here.",
        "author_id": "author-123",
    }
    defaults.update(overrides)
    return Article.create(**defaults)


def test_should_create_article_with_valid_fields():
    article = _create_article()
    assert article.id != ""
    assert article.title == "My First Article"
    assert article.description == "A short description"
    assert article.content == "Full article content here."
    assert article.author_id == "author-123"
    assert article.created_at is not None
    assert article.updated_at is not None


def test_should_generate_slug_from_title_on_create():
    article = _create_article(title="My Awesome Post")
    assert article.slug == "my-awesome-post"


def test_should_start_unpublished_on_create():
    article = _create_article()
    assert article.published is False


def test_should_record_article_created_event():
    article = _create_article()
    events = article.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ArticleCreated)
    assert events[0].article_id == article.id
    assert events[0].event_type == ARTICLE_CREATED_EVENT


def test_should_default_tags_to_empty_list():
    article = _create_article()
    assert article.tags == []


def test_should_default_category_to_none():
    article = _create_article()
    assert article.category_id is None


def test_should_accept_tags_and_category_on_create():
    article = _create_article(category_id="cat-1", tags=["tag-1", "tag-2"])
    assert article.category_id == "cat-1"
    assert article.tags == ["tag-1", "tag-2"]


def test_should_update_title_and_regenerate_slug():
    article = _create_article()
    article.pull_domain_events()  # drain creation event
    article.update({"title": "Updated Title"})
    assert article.title == "Updated Title"
    assert article.slug == "updated-title"


def test_should_update_description_and_content():
    article = _create_article()
    article.pull_domain_events()
    article.update({"description": "New desc", "content": "New content"})
    assert article.description == "New desc"
    assert article.content == "New content"


def test_should_update_category_and_tags():
    article = _create_article()
    article.pull_domain_events()
    article.update({"category_id": "cat-99", "tags": ["t1"]})
    assert article.category_id == "cat-99"
    assert article.tags == ["t1"]


def test_should_record_article_updated_event():
    article = _create_article()
    article.pull_domain_events()
    payload = {"title": "Changed"}
    article.update(payload)
    events = article.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ArticleUpdated)
    assert events[0].article_id == article.id
    assert events[0].event_type == ARTICLE_UPDATED_EVENT
    assert events[0].payload == {"title": "Changed"}


def test_should_publish_article():
    article = _create_article()
    article.pull_domain_events()
    article.publish()
    assert article.published is True
    events = article.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ArticlePublished)
    assert events[0].article_id == article.id
    assert events[0].event_type == ARTICLE_PUBLISHED_EVENT


def test_should_unpublish_article():
    article = _create_article()
    article.publish()
    article.pull_domain_events()
    article.unpublish()
    assert article.published is False
    events = article.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ArticleUnpublished)
    assert events[0].article_id == article.id
    assert events[0].event_type == ARTICLE_UNPUBLISHED_EVENT


def test_should_clear_events_after_pull():
    article = _create_article()
    first_pull = article.pull_domain_events()
    second_pull = article.pull_domain_events()
    assert len(first_pull) == 1
    assert len(second_pull) == 0
