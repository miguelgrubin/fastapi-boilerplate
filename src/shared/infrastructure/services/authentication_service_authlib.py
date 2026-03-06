from typing import Optional

from authlib.integrations.starlette_client import OAuth
from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.domain.services.authentication_service import AuthenticationService
from starlette.requests import Request
from starlette.responses import RedirectResponse


class AuthenticationServiceAuthlib(AuthenticationService):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        issuer_url: str,
    ) -> None:
        self._oauth = OAuth()
        self._oauth.register(
            name="authelia",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f"{issuer_url}/.well-known/openid-configuration",
            client_kwargs={"scope": "openid profile email groups"},
        )

    async def get_login_redirect(self, request: Request) -> RedirectResponse:
        redirect_uri = request.url_for("auth_callback")
        return await self._oauth.authelia.authorize_redirect(request, str(redirect_uri))

    async def handle_callback(self, request: Request) -> AuthenticatedUser:
        token = await self._oauth.authelia.authorize_access_token(request)
        userinfo = token.get("userinfo", {})

        user = AuthenticatedUser(
            sub=userinfo.get("sub", ""),
            username=userinfo.get("preferred_username", ""),
            email=userinfo.get("email", ""),
            groups=userinfo.get("groups", []),
            name=userinfo.get("name", ""),
        )

        request.session["user"] = {
            "sub": user.sub,
            "username": user.username,
            "email": user.email,
            "groups": user.groups,
            "name": user.name,
        }

        return user

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
