import uuid

from src.blog.domain.tag import Tag


def test_should_create_tag_with_valid_fields():
    tag = Tag.create("Python")
    assert tag.name == "Python"
    assert tag.slug == "python"
    assert tag.created_at is not None


def test_should_generate_slug_from_name():
    tag = Tag.create("Machine Learning")
    assert tag.slug == "machine-learning"


def test_should_generate_uuid_as_id():
    tag = Tag.create("FastAPI")
    parsed = uuid.UUID(tag.id)
    assert str(parsed) == tag.id
