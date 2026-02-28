import uuid

from src.blog.domain.category import Category


def test_should_create_category_with_valid_fields():
    category = Category.create("Technology")
    assert category.name == "Technology"
    assert category.slug == "technology"
    assert category.created_at is not None


def test_should_generate_slug_from_name():
    category = Category.create("Web Development")
    assert category.slug == "web-development"


def test_should_generate_uuid_as_id():
    category = Category.create("Science")
    # Verify the id is a valid UUID string
    parsed = uuid.UUID(category.id)
    assert str(parsed) == category.id
