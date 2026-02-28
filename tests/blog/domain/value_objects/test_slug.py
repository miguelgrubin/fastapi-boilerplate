from dataclasses import FrozenInstanceError

import pytest
from src.blog.domain.value_objects.slug import Slug


def test_should_convert_to_lowercase():
    slug = Slug.from_name("Hello World")
    assert slug.value == "hello-world"


def test_should_replace_spaces_with_hyphens():
    slug = Slug.from_name("my fav post")
    assert slug.value == "my-fav-post"


def test_should_strip_special_characters():
    slug = Slug.from_name("Hello, World! How's it going?")
    assert slug.value == "hello-world-hows-it-going"


def test_should_collapse_consecutive_hyphens():
    slug = Slug.from_name("a--b---c")
    assert slug.value == "a-b-c"


def test_should_strip_leading_and_trailing_hyphens():
    slug = Slug.from_name(" -hello- ")
    assert slug.value == "hello"


def test_should_handle_numbers_by_removing_them():
    slug = Slug.from_name("post123")
    assert slug.value == "post"


def test_should_be_immutable():
    slug = Slug.from_name("test")
    with pytest.raises(FrozenInstanceError):
        slug.value = "changed"


def test_should_handle_empty_string():
    slug = Slug.from_name("")
    assert slug.value == ""


def test_should_handle_only_special_characters():
    slug = Slug.from_name("@#$%^&*()")
    assert slug.value == ""
