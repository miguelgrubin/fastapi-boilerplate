from typing import Callable, Optional

from fastapi import Depends, Request
from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.domain.errors.forbidden import Forbidden
from src.shared.domain.errors.unauthorized import Unauthorized
from src.shared.domain.services.authentication_service import AuthenticationService
from src.shared.domain.services.authorization_service import AuthorizationService


def create_get_current_user(
    authentication_service: AuthenticationService,
) -> Callable:
    async def get_current_user(request: Request) -> AuthenticatedUser:
        user = await authentication_service.get_current_user(request)
        if user is None:
            raise Unauthorized()
        return user

    return get_current_user


def create_get_optional_user(
    authentication_service: AuthenticationService,
) -> Callable:
    async def get_optional_user(request: Request) -> Optional[AuthenticatedUser]:
        return await authentication_service.get_current_user(request)

    return get_optional_user


def create_require_authorization(
    authorization_service: AuthorizationService,
    authentication_service: AuthenticationService,
) -> Callable:
    get_current_user = create_get_current_user(authentication_service)

    def require_authorization(resource: str, action: str) -> Callable:
        async def check_authorization(
            request: Request,
            current_user: AuthenticatedUser = Depends(get_current_user),
        ) -> AuthenticatedUser:
            for group in current_user.groups:
                if authorization_service.enforce(group, resource, action):
                    return current_user
            raise Forbidden()

        return check_authorization

    return require_authorization
