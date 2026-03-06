from src.shared.infrastructure.services.authorization_service_fake import (
    AuthorizationServiceFake,
)


def test_should_allow_all_when_configured():
    service = AuthorizationServiceFake(allow_all=True)
    assert service.enforce("anyone", "/any/path", "any_action") is True


def test_should_deny_all_when_configured():
    service = AuthorizationServiceFake(allow_all=False)
    assert service.enforce("anyone", "/any/path", "any_action") is False


def test_should_add_and_get_roles():
    service = AuthorizationServiceFake()
    service.add_role_for_user("user1", "admin")
    roles = service.get_roles_for_user("user1")
    assert "admin" in roles


def test_should_return_empty_roles_for_unknown_user():
    service = AuthorizationServiceFake()
    roles = service.get_roles_for_user("unknown")
    assert roles == []


def test_should_not_duplicate_roles():
    service = AuthorizationServiceFake()
    assert service.add_role_for_user("user1", "admin") is True
    assert service.add_role_for_user("user1", "admin") is False
    roles = service.get_roles_for_user("user1")
    assert len(roles) == 1
