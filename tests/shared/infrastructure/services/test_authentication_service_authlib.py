from unittest.mock import AsyncMock, MagicMock

from src.shared.infrastructure.services.authentication_service_authlib import (
    AuthenticationServiceAuthlib,
)
from starlette.requests import Request


async def test_should_store_user_in_session_on_callback():
    """Test that handle_callback stores user info in session."""
    service = AuthenticationServiceAuthlib.__new__(AuthenticationServiceAuthlib)

    mock_oauth = MagicMock()
    service._oauth = mock_oauth

    mock_token = {
        "userinfo": {
            "sub": "user-123",
            "preferred_username": "admin",
            "email": "admin@example.com",
            "groups": ["admins"],
            "name": "Admin User",
        }
    }
    mock_oauth.authelia.authorize_access_token = AsyncMock(return_value=mock_token)

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.handle_callback(mock_request)

    assert user.sub == "user-123"
    assert user.username == "admin"
    assert user.email == "admin@example.com"
    assert user.groups == ["admins"]
    assert user.name == "Admin User"
    assert mock_request.session["user"]["sub"] == "user-123"


async def test_should_return_user_from_session():
    """Test that get_current_user reads from session."""
    service = AuthenticationServiceAuthlib.__new__(AuthenticationServiceAuthlib)
    service._oauth = MagicMock()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {
        "user": {
            "sub": "user-123",
            "username": "admin",
            "email": "admin@example.com",
            "groups": ["admins"],
            "name": "Admin User",
        }
    }

    user = await service.get_current_user(mock_request)

    assert user is not None
    assert user.sub == "user-123"
    assert user.username == "admin"


async def test_should_return_none_when_no_session():
    """Test that get_current_user returns None when no session data."""
    service = AuthenticationServiceAuthlib.__new__(AuthenticationServiceAuthlib)
    service._oauth = MagicMock()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {}

    user = await service.get_current_user(mock_request)

    assert user is None


async def test_should_clear_session_on_logout():
    """Test that logout clears the session."""
    service = AuthenticationServiceAuthlib.__new__(AuthenticationServiceAuthlib)
    service._oauth = MagicMock()

    mock_request = MagicMock(spec=Request)
    mock_request.session = {
        "user": {
            "sub": "user-123",
            "username": "admin",
            "email": "admin@example.com",
            "groups": ["admins"],
            "name": "Admin User",
        }
    }

    await service.logout(mock_request)

    assert mock_request.session == {}
