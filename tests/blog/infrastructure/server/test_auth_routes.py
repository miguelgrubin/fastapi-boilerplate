from unittest.mock import MagicMock

from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.infrastructure.services.authentication_service_fake import (
    AuthenticationServiceFake,
)
from starlette.requests import Request
from starlette.responses import RedirectResponse


async def test_should_return_redirect_on_login():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    response = await service.get_login_redirect(mock_request)

    assert isinstance(response, RedirectResponse)


async def test_should_return_user_on_callback():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.handle_callback(mock_request)

    assert isinstance(user, AuthenticatedUser)
    assert user.username == "testuser"


async def test_should_clear_session_on_logout():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {"user": {"sub": "123"}}

    response = await service.logout(mock_request)

    assert isinstance(response, RedirectResponse)
    assert mock_request.session == {}


async def test_should_return_none_when_no_session_user():
    service = AuthenticationServiceFake()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.get_current_user(mock_request)

    assert user is None
