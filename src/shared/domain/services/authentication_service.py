from typing import Optional

from abc import ABC, abstractmethod

from src.shared.domain.authenticated_user import AuthenticatedUser
from starlette.requests import Request
from starlette.responses import RedirectResponse

AUTHENTICATION_SERVICE = "AuthenticationService"


class AuthenticationService(ABC):
    @abstractmethod
    async def get_login_redirect(self, request: Request) -> RedirectResponse:
        pass

    @abstractmethod
    async def handle_callback(self, request: Request) -> AuthenticatedUser:
        pass

    @abstractmethod
    async def get_current_user(self, request: Request) -> Optional[AuthenticatedUser]:
        pass

    @abstractmethod
    async def logout(self, request: Request) -> RedirectResponse:
        pass
