from unittest.mock import MagicMock

from src.shared.infrastructure.services.authentication_service_fake import (
    AuthenticationServiceFake,
)
from starlette.requests import Request


async def test_should_return_fake_user_on_callback():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.handle_callback(mock_request)

    assert user.sub == "fake-sub-id"
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.groups == ["admins"]


async def test_should_store_user_in_session():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    await service.handle_callback(mock_request)

    assert mock_request.session["user"]["username"] == "testuser"


async def test_should_return_user_from_session():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {
        "user": {
            "sub": "fake-sub-id",
            "username": "testuser",
            "email": "testuser@example.com",
            "groups": ["admins"],
            "name": "Test User",
        }
    }

    user = await service.get_current_user(mock_request)

    assert user is not None
    assert user.username == "testuser"


async def test_should_return_none_when_no_session():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.get_current_user(mock_request)

    assert user is None
