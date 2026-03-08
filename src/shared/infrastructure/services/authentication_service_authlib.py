import logging
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from src.shared.domain.authenticated_user import AuthenticatedUser
from src.shared.domain.services.authentication_service import AuthenticationService
from starlette.requests import Request
from starlette.responses import RedirectResponse

logger = logging.getLogger(__name__)


class AuthenticationServiceAuthlib(AuthenticationService):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        issuer_url: str,
        verify_ssl: bool = True,
    ) -> None:
        self._oauth = OAuth()
        client_kwargs: dict[str, object] = {
            "scope": "openid profile email groups",
            "token_endpoint_auth_method": "client_secret_post",
        }
        if not verify_ssl:
            client_kwargs["verify"] = False
        self._oauth.register(
            name="authelia",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f"{issuer_url}/.well-known/openid-configuration",
            client_kwargs=client_kwargs,
        )

    async def get_login_redirect(self, request: Request) -> RedirectResponse:
        redirect_uri = request.url_for("auth_callback")
        return await self._oauth.authelia.authorize_redirect(request, str(redirect_uri))

    async def handle_callback(self, request: Request) -> AuthenticatedUser:
        token = await self._oauth.authelia.authorize_access_token(request)

        # Try userinfo from token response first, then explicit endpoint call,
        # then fall back to ID token claims
        userinfo = token.get("userinfo")
        if not userinfo or not userinfo.get("preferred_username"):
            logger.debug("Token userinfo missing or incomplete, calling userinfo endpoint")
            try:
                userinfo = await self._oauth.authelia.userinfo(token=token)
            except Exception:
                logger.warning("Userinfo endpoint call failed", exc_info=True)
                userinfo = None

        if not userinfo or not userinfo.get("preferred_username"):
            logger.debug("Userinfo still missing, falling back to ID token claims")
            userinfo = dict(token)

        logger.debug("Final userinfo keys: %s", list(userinfo.keys()) if userinfo else None)

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
