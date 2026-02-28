import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.domain.errors.category_already_exists import CategoryAlreadyExists
from src.blog.domain.errors.category_not_found import CategoryNotFound
from src.blog.domain.errors.comment_not_found import CommentNotFound
from src.blog.domain.errors.tag_already_exists import TagAlreadyExists
from src.blog.domain.errors.tag_not_found import TagNotFound
from src.blog.domain.errors.user_already_exists import UserAlreadyExists
from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.errors.user_not_found import UserNotFound


def test_article_not_found_should_format_message_and_store_id():
    error = ArticleNotFound("art-123")
    assert str(error) == "Article with ID art-123 not found."
    assert error.article_id == "art-123"


def test_user_already_exists_should_format_message():
    error = UserAlreadyExists("duplicate email")
    assert str(error) == "User already exists. duplicate email"


def test_user_not_found_should_format_message_and_store_id():
    error = UserNotFound("user-456")
    assert str(error) == "User with ID user-456 not found."
    assert error.user_id == "user-456"


def test_user_not_following_should_format_message():
    error = UserNotFollowing("user-789")
    assert "user-789" in str(error)
    assert "can not be unfollowed" in str(error)


def test_comment_not_found_should_format_message_and_store_id():
    error = CommentNotFound("com-111")
    assert str(error) == "Comment with ID com-111 not found."
    assert error.comment_id == "com-111"


def test_category_not_found_should_format_message_and_store_id():
    error = CategoryNotFound("cat-222")
    assert str(error) == "Category with ID cat-222 not found."
    assert error.category_id == "cat-222"


def test_category_already_exists_should_format_message():
    error = CategoryAlreadyExists("duplicate name")
    assert str(error) == "Category already exists. duplicate name"


def test_tag_not_found_should_format_message_and_store_id():
    error = TagNotFound("tag-333")
    assert str(error) == "Tag with ID tag-333 not found."
    assert error.tag_id == "tag-333"


def test_tag_already_exists_should_format_message():
    error = TagAlreadyExists("duplicate slug")
    assert str(error) == "Tag already exists. duplicate slug"


def test_all_errors_are_exceptions():
    errors = [
        ArticleNotFound("x"),
        UserAlreadyExists("x"),
        UserNotFound("x"),
        UserNotFollowing("x"),
        CommentNotFound("x"),
        CategoryNotFound("x"),
        CategoryAlreadyExists("x"),
        TagNotFound("x"),
        TagAlreadyExists("x"),
    ]
    for error in errors:
        assert isinstance(error, Exception)


def test_errors_can_be_raised_and_caught():
    with pytest.raises(ArticleNotFound):
        raise ArticleNotFound("art-1")

    with pytest.raises(UserNotFound):
        raise UserNotFound("user-1")

    with pytest.raises(CommentNotFound):
        raise CommentNotFound("com-1")
