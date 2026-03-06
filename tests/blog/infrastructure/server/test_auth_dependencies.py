from unittest.mock import MagicMock

import pytest
from src.blog.infrastructure.server.auth_dependencies import (
    create_get_current_user,
    create_get_optional_user,
    create_require_authorization,
)
from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.domain.errors.forbidden import Forbidden
from src.shared.domain.errors.unauthorized import Unauthorized
from src.shared.infrastructure.services.authentication_service_fake import (
    AuthenticationServiceFake,
)
from src.shared.infrastructure.services.authorization_service_fake import (
    AuthorizationServiceFake,
)


def _create_authenticated_request():
    mock_request = MagicMock()
    mock_request.session = {
        "user": {
            "sub": "user-123",
            "username": "admin",
            "email": "admin@example.com",
            "groups": ["admins"],
            "name": "Admin User",
        }
    }
    return mock_request


def _create_unauthenticated_request():
    mock_request = MagicMock()
    mock_request.session = {}
    return mock_request


async def test_should_return_user_when_authenticated():
    auth_service = AuthenticationServiceFake()
    get_current_user = create_get_current_user(auth_service)

    request = _create_authenticated_request()
    user = await get_current_user(request)

    assert isinstance(user, AuthenticatedUser)
    assert user.username == "admin"


async def test_should_raise_unauthorized_when_not_authenticated():
    auth_service = AuthenticationServiceFake()
    get_current_user = create_get_current_user(auth_service)

    request = _create_unauthenticated_request()
    with pytest.raises(Unauthorized):
        await get_current_user(request)


async def test_should_return_none_for_optional_user_when_not_authenticated():
    auth_service = AuthenticationServiceFake()
    get_optional_user = create_get_optional_user(auth_service)

    request = _create_unauthenticated_request()
    user = await get_optional_user(request)

    assert user is None


async def test_should_return_user_for_optional_user_when_authenticated():
    auth_service = AuthenticationServiceFake()
    get_optional_user = create_get_optional_user(auth_service)

    request = _create_authenticated_request()
    user = await get_optional_user(request)

    assert user is not None
    assert user.username == "admin"


async def test_should_allow_authorized_user():
    auth_service = AuthenticationServiceFake()
    authz_service = AuthorizationServiceFake(allow_all=True)
    require_authorization = create_require_authorization(authz_service, auth_service)

    check = require_authorization("/app/v1/blog/articles", "read")
    request = _create_authenticated_request()

    user = AuthenticatedUser(
        sub="user-123",
        username="admin",
        email="admin@example.com",
        groups=["admins"],
        name="Admin User",
    )

    result = await check(request, current_user=user)
    assert result.username == "admin"


async def test_should_raise_forbidden_when_not_authorized():
    auth_service = AuthenticationServiceFake()
    authz_service = AuthorizationServiceFake(allow_all=False)
    require_authorization = create_require_authorization(authz_service, auth_service)

    check = require_authorization("/app/v1/blog/articles", "read")
    request = _create_authenticated_request()

    user = AuthenticatedUser(
        sub="user-123",
        username="admin",
        email="admin@example.com",
        groups=["admins"],
        name="Admin User",
    )

    with pytest.raises(Forbidden):
        await check(request, current_user=user)
