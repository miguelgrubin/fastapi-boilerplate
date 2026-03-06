from fastapi import FastAPI
from src.shared.domain.services.authentication_service import AuthenticationService
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse


def auth_routes(app: FastAPI, authentication_service: AuthenticationService) -> None:
    @app.get("/auth/login")
    async def auth_login(request: Request) -> RedirectResponse:
        return await authentication_service.get_login_redirect(request)

    @app.get("/auth/callback", name="auth_callback")
    async def auth_callback(request: Request) -> RedirectResponse:
        await authentication_service.handle_callback(request)
        return RedirectResponse(url="/docs")

    @app.get("/auth/logout")
    async def auth_logout(request: Request) -> RedirectResponse:
        return await authentication_service.logout(request)

    @app.get("/auth/me")
    async def auth_me(request: Request) -> JSONResponse:
        user = await authentication_service.get_current_user(request)
        if not user:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
        return JSONResponse(
            content={
                "sub": user.sub,
                "username": user.username,
                "email": user.email,
                "groups": user.groups,
                "name": user.name,
            }
        )
