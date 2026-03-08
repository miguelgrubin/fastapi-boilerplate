import os

from src.shared.infrastructure.services.authorization_service_casbin import (
    AuthorizationServiceCasbin,
)

_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src", "config")
_MODEL_PATH = os.path.join(_CONFIG_DIR, "casbin_model.conf")
_POLICY_PATH = os.path.join(_CONFIG_DIR, "casbin_policy.conf")


def _create_service() -> AuthorizationServiceCasbin:
    return AuthorizationServiceCasbin(
        model_path=_MODEL_PATH,
        policy_path=_POLICY_PATH,
    )


# ---- Admin role tests ----


def test_should_allow_admin_access_to_admin_endpoints():
    service = _create_service()
    assert service.enforce("admin", "/admin/v1/blog/users", "write") is True


def test_should_allow_admin_access_to_app_endpoints():
    service = _create_service()
    assert service.enforce("admin", "/app/v1/blog/articles", "read") is True
    assert service.enforce("admin", "/app/v1/blog/articles", "write") is True


# ---- User role tests ----


def test_should_allow_user_to_read_articles():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/articles", "read") is True


def test_should_allow_user_to_read_single_article():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/articles/123", "read") is True


def test_should_deny_user_write_to_articles():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/articles", "write") is False


def test_should_allow_user_to_read_categories():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/categories", "read") is True


def test_should_allow_user_to_read_tags():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/tags", "read") is True


def test_should_allow_user_to_read_comments():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/articles/123/comments", "read") is True


def test_should_allow_user_to_write_comments():
    service = _create_service()
    assert service.enforce("user", "/app/v1/blog/articles/123/comments", "write") is True


def test_should_deny_user_access_to_admin_endpoints():
    service = _create_service()
    assert service.enforce("user", "/admin/v1/blog/users", "write") is False


# ---- Group-to-role mapping tests ----


def test_should_map_admins_group_to_admin_role():
    service = _create_service()
    assert service.enforce("admins", "/admin/v1/blog/users", "write") is True
    assert service.enforce("admins", "/app/v1/blog/articles", "read") is True


def test_should_map_users_group_to_user_role():
    service = _create_service()
    assert service.enforce("users", "/app/v1/blog/articles", "read") is True
    assert service.enforce("users", "/admin/v1/blog/users", "write") is False


# ---- Role management tests ----


def test_should_get_roles_for_admins_group():
    service = _create_service()
    roles = service.get_roles_for_user("admins")
    assert "admin" in roles


def test_should_get_roles_for_users_group():
    service = _create_service()
    roles = service.get_roles_for_user("users")
    assert "user" in roles


def test_should_add_role_for_user():
    service = _create_service()
    result = service.add_role_for_user("newgroup", "user")
    assert result is True
    assert service.enforce("newgroup", "/app/v1/blog/articles", "read") is True


# ---- Deny by default tests ----


def test_should_deny_unknown_subject():
    service = _create_service()
    assert service.enforce("unknown", "/app/v1/blog/articles", "read") is False


def test_should_deny_unknown_resource():
    service = _create_service()
    assert service.enforce("admin", "/unknown/path", "read") is False
