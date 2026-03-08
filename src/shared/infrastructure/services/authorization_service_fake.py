from typing import List

from src.shared.domain.services.authorization_service import AuthorizationService


class AuthorizationServiceFake(AuthorizationService):
    def __init__(self, allow_all: bool = True) -> None:
        self._allow_all = allow_all
        self._roles: dict[str, list[str]] = {}

    def enforce(self, subject: str, resource: str, action: str) -> bool:
        return self._allow_all

    def get_roles_for_user(self, user: str) -> List[str]:
        return self._roles.get(user, [])

    def add_role_for_user(self, user: str, role: str) -> bool:
        if user not in self._roles:
            self._roles[user] = []
        if role not in self._roles[user]:
            self._roles[user].append(role)
            return True
        return False
