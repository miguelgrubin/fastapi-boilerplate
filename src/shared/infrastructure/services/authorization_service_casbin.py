from typing import List

import casbin
from src.shared.domain.services.authorization_service import AuthorizationService


class AuthorizationServiceCasbin(AuthorizationService):
    def __init__(self, model_path: str, policy_path: str) -> None:
        self._enforcer = casbin.Enforcer(model_path, policy_path)

    def enforce(self, subject: str, resource: str, action: str) -> bool:
        return self._enforcer.enforce(subject, resource, action)

    def get_roles_for_user(self, user: str) -> List[str]:
        return self._enforcer.get_roles_for_user(user)

    def add_role_for_user(self, user: str, role: str) -> bool:
        return self._enforcer.add_role_for_user(user, role)
