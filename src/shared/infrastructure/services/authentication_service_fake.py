from typing import Optional

from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.domain.services.authentication_service import AuthenticationService
from starlette.requests import Request
from starlette.responses import RedirectResponse


class AuthenticationServiceFake(AuthenticationService):
    def __init__(self) -> None:
        self._user = AuthenticatedUser(
            sub="fake-sub-id",
            username="testuser",
            email="testuser@example.com",
            groups=["admins"],
            name="Test User",
        )

    async def get_login_redirect(self, request: Request) -> RedirectResponse:
        return RedirectResponse(url="/auth/callback")

    async def handle_callback(self, request: Request) -> AuthenticatedUser:
        request.session["user"] = {
            "sub": self._user.sub,
            "username": self._user.username,
            "email": self._user.email,
            "groups": self._user.groups,
            "name": self._user.name,
        }
        return self._user

    async def get_current_user(self, request: Request) -> Optional[AuthenticatedUser]:
        user_data = request.session.get("user")
        if not user_data:
            return None
        return AuthenticatedUser(
            sub=user_data["sub"],
            username=user_data["username"],
            email=user_data["email"],
            groups=user_data["groups"],
            name=user_data["name"],
        )

    async def logout(self, request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse(url="/")
