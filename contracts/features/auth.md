# Authentication & Authorization

## Overview

Replace the Traefik forward-auth proxy authentication with app-level authentication and authorization:
- **Authelia** becomes an OpenID Connect 1.0 Provider (identity provider)
- **Authlib** (in FastAPI) becomes the OIDC Relying Party (client) - handles login flows and token validation
- **PyCasbin** enforces RBAC authorization on API endpoints
- Existing user creation with passwords is kept alongside OIDC

## Architecture Flow

```
User -> FastAPI (Authlib OIDC client) -> Authelia (OIDC Provider)
                                              |
                                       user authenticates
                                              |
User <- FastAPI receives ID token + access token
                |
         PyCasbin RBAC checks (user groups -> roles -> permissions)
```

---

## Phase 1: Authelia OpenID Connect Provider Configuration

**Files to modify:**

1. **`docker/authelia/config/configuration.yml`** - Add `identity_providers.oidc` section:
   - Generate RSA keypair for JWT signing (`jwks`)
   - Set `hmac_secret`
   - Register FastAPI as a client with:
     - `client_id: 'fastapi-blog'`
     - `client_secret` (hashed)
     - `redirect_uris: ['https://blog.localtest.me/auth/callback']`
     - `scopes: ['openid', 'profile', 'email', 'groups']`
     - `grant_types: ['authorization_code', 'refresh_token']`
     - `response_types: ['code']`
     - `consent_mode: 'implicit'` (dev-friendly, no consent screen)
     - `token_endpoint_auth_method: 'client_secret_post'`

2. **`docker/authelia/secrets/`** - Add RSA private key file for OIDC JWT signing

3. **`.env`, `.env.example`, `.env.docker`** - Add new env vars:
   - `OIDC_CLIENT_ID`
   - `OIDC_CLIENT_SECRET`
   - `OIDC_ISSUER_URL` (e.g., `https://auth.localtest.me`)
   - `AUTHELIA_OIDC_HMAC_SECRET`

4. **`compose.yml`** - Update:
   - Remove Authelia `forwardAuth` middleware from Traefik labels on the `app` service
   - Keep Authelia running as the OIDC provider
   - Pass OIDC env vars to the FastAPI `app` container
   - Add `SessionMiddleware` secret to app env vars

---

## Phase 2: AuthenticationService (Authlib OIDC Client in FastAPI)

**New files (following hexagonal architecture):**

5. **`src/shared/domain/services/authentication_service.py`** - ABC port:
   ```python
   class AuthenticationService(ABC):
       @abstractmethod
       async def get_login_redirect(self, request: Request) -> RedirectResponse: ...

       @abstractmethod
       async def handle_callback(self, request: Request) -> AuthenticatedUser: ...

       @abstractmethod
       async def get_current_user(self, request: Request) -> Optional[AuthenticatedUser]: ...

       @abstractmethod
       async def logout(self, request: Request) -> RedirectResponse: ...
   ```

6. **`src/shared/domain/authenticated_user.py`** - Value object:
   ```python
   @dataclass(frozen=True)
   class AuthenticatedUser:
       sub: str           # OIDC subject identifier
       username: str
       email: str
       groups: List[str]  # Maps to Authelia groups -> Casbin roles
       name: str
   ```

7. **`src/shared/infrastructure/services/authentication_service_authlib.py`** - Authlib implementation:
   - Registers Authelia as an OIDC provider via `authlib.integrations.starlette_client.OAuth`
   - Uses `server_metadata_url` for auto-discovery (`/.well-known/openid-configuration`)
   - Implements Authorization Code flow with PKCE
   - Stores tokens in session (Starlette `SessionMiddleware`)
   - Validates ID tokens and extracts user info
   - Implements `get_current_user()` to read session and return `AuthenticatedUser`

8. **`src/shared/infrastructure/services/authentication_service_fake.py`** - Fake for testing:
   - Returns a hardcoded `AuthenticatedUser` without OIDC flow
   - Useful for test isolation

---

## Phase 3: AuthorizationService (PyCasbin RBAC)

**New files:**

9. **`src/shared/domain/services/authorization_service.py`** - ABC port:
   ```python
   class AuthorizationService(ABC):
       @abstractmethod
       def enforce(self, subject: str, resource: str, action: str) -> bool: ...

       @abstractmethod
       def get_roles_for_user(self, user: str) -> List[str]: ...

       @abstractmethod
       def add_role_for_user(self, user: str, role: str) -> bool: ...
   ```

10. **`src/shared/infrastructure/services/authorization_service_casbin.py`** - Casbin implementation:
    - Loads RBAC model from `casbin_model.conf`
    - Loads policies from `casbin_policy.csv`
    - Maps Authelia groups to Casbin roles
    - `enforce()` calls `casbin.Enforcer.enforce(sub, obj, act)`

11. **`src/shared/infrastructure/services/authorization_service_fake.py`** - Fake for testing:
    - Always permits (or configurable behavior)

12. **`src/config/casbin_model.conf`** - RBAC model definition:
    ```ini
    [request_definition]
    r = sub, obj, act

    [policy_definition]
    p = sub, obj, act

    [role_definition]
    g = _, _

    [policy_effect]
    e = some(where (p.eft == allow))

    [matchers]
    m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && r.act == p.act
    ```

13. **`src/config/casbin_policy.csv`** - RBAC policies:
    ```csv
    p, admin, /admin/*, *
    p, admin, /app/*, *
    p, user, /app/v1/blog/articles, read
    p, user, /app/v1/blog/articles/*, read
    p, user, /app/v1/blog/categories, read
    p, user, /app/v1/blog/tags, read
    p, user, /app/v1/blog/articles/*/comments, read
    p, user, /app/v1/blog/articles/*/comments, write
    g, admins, admin
    g, users, user
    ```

---

## Phase 4: FastAPI Integration (Routes, Middleware, Dependencies)

**Files to modify/create:**

14. **`src/settings.py`** - Add OIDC and auth configuration:
    - `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_ISSUER_URL`
    - `SESSION_SECRET_KEY`
    - `CASBIN_MODEL_PATH`, `CASBIN_POLICY_PATH`

15. **`src/http_server.py`** - Add:
    - `SessionMiddleware` for OIDC session storage
    - Auth routes (`/auth/login`, `/auth/callback`, `/auth/logout`, `/auth/me`)

16. **`src/blog/infrastructure/server/auth_routes.py`** - New auth routes:
    - `GET /auth/login` - Initiates OIDC Authorization Code flow via Authlib
    - `GET /auth/callback` - Handles OIDC callback, stores tokens in session
    - `GET /auth/logout` - Clears session, redirects to Authelia end-session
    - `GET /auth/me` - Returns current user info from session

17. **`src/blog/infrastructure/server/auth_dependencies.py`** - FastAPI dependencies:
    - `get_current_user(request)` - Extracts `AuthenticatedUser` from session, returns 401 if not authenticated
    - `require_authorization(resource, action)` - Factory that returns a dependency checking Casbin
    - `get_optional_user(request)` - Returns `None` if not authenticated (for public endpoints)

18. **`src/blog/infrastructure/server/router.py`** - Modify:
    - Add `Depends(get_current_user)` to protected routes
    - Add `Depends(require_authorization(...))` for RBAC enforcement
    - Keep public routes (docs, health, article listing) without auth
    - Pass authenticated user to use cases that need it (article creation, etc.)

19. **`src/shared/types.py`** - Add `authentication_service` and `authorization_service` to `SharedServices`

20. **`src/shared/factory.py`** - Add factory functions:
    - `create_authentication_service(settings)` -> `AuthenticationServiceAuthlib`
    - `create_authorization_service(model_path, policy_path)` -> `AuthorizationServiceCasbin`

21. **`src/blog/factory.py`** - Wire new services into the composition root

22. **`src/blog/types.py`** - Update `BlogUseCasesType` if use cases need auth context

---

## Phase 5: Dependencies and Configuration

23. **`pyproject.toml`** - Add dependencies:
    - `authlib` - OIDC client + JOSE utilities
    - `httpx` - Required by Authlib's async Starlette/FastAPI integration
    - `casbin` - PyCasbin RBAC engine
    - `itsdangerous` - Required by Starlette `SessionMiddleware`

---

## Phase 6: Update Docker/Traefik Configuration

24. **`docker/traefik/config/dynamic.yml`** - Remove or simplify the `authelia` forwardAuth middleware (no longer needed for API protection; Authelia is now just the OIDC IdP)

25. **`compose.yml`** - Remove `authelia@file` middleware from FastAPI app Traefik labels; keep Authelia service running as OIDC provider

---

## Phase 7: Tests

26. **`tests/shared/infrastructure/services/test_authentication_service_authlib.py`** - Test token parsing, session handling
27. **`tests/shared/infrastructure/services/test_authorization_service_casbin.py`** - Test RBAC enforcement, role mapping
28. **`tests/blog/infrastructure/server/test_auth_routes.py`** - Test login redirect, callback, logout
29. **`tests/blog/infrastructure/server/test_auth_dependencies.py`** - Test dependency injection, 401 on unauthenticated, 403 on unauthorized
30. Update existing tests that hit protected routes to use the fake auth services

---

## Phase 8: Domain Error Classes

31. **`src/shared/domain/errors/unauthorized.py`** - `Unauthorized` exception (401)
32. **`src/shared/domain/errors/forbidden.py`** - `Forbidden` exception (403)
33. **`src/blog/infrastructure/server/error_handler.py`** - Register handlers for these new exceptions

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| AuthenticationService as ABC port in domain | Follows hexagonal architecture - domain doesn't depend on Authlib |
| AuthorizationService as ABC port in domain | Follows hexagonal architecture - domain doesn't depend on Casbin |
| Session-based token storage | Standard for server-rendered OIDC flows; Authlib's Starlette integration uses sessions |
| File-based Casbin policies | Simple, version-controlled, fits boilerplate nature |
| `keyMatch2` matcher in Casbin | Supports URL path patterns like `/app/v1/blog/articles/:id` |
| Keep PasswordService + UserCreator | Users can still be created/managed in-app; OIDC adds external auth |
| Fake implementations for testing | Maintains test isolation without needing a running Authelia instance |

## Execution Order

1. Phase 5 (dependencies) - needed first
2. Phase 1 (Authelia OIDC config) - infrastructure prerequisite
3. Phase 8 (domain errors) - small, foundational
4. Phase 2 (AuthenticationService) - core auth
5. Phase 3 (AuthorizationService) - core authz
6. Phase 4 (FastAPI integration) - wiring everything together
7. Phase 6 (Docker/Traefik updates) - cleanup
8. Phase 7 (tests) - verify everything works
