from unittest.mock import patch

import pytest
from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake


def _create_repository():
    repository = UserRepositoryMemory()
    repository.clear()
    return repository


def _create_user(repository: UserRepositoryMemory):
    password_service = PasswordServiceFake()
    creator = UserCreator(repository, password_service)
    return creator.execute("someone", "S3CUR€ PA$$", "someone@example.com")


def test_should_delete_user_when_user_exists():
    repository = _create_repository()
    user = _create_user(repository)
    use_case = UserDeleter(repository)

    result = use_case.execute(user.id)

    assert result is None
    assert repository.find_one(user.id) is None


def test_should_raise_error_when_user_not_found():
    repository = _create_repository()
    use_case = UserDeleter(repository)

    with pytest.raises(UserNotFound):
        use_case.execute("non-existent-id")


@patch.object(UserRepositoryMemory, "delete")
def test_should_call_delete_on_repository(mock_delete):
    repository = _create_repository()
    user = _create_user(repository)
    use_case = UserDeleter(repository)

    use_case.execute(user.id)

    mock_delete.assert_called_with(user.id)
