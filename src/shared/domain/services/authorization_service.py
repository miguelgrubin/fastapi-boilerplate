from typing import List

from abc import ABC, abstractmethod

AUTHORIZATION_SERVICE = "AuthorizationService"


class AuthorizationService(ABC):
    @abstractmethod
    def enforce(self, subject: str, resource: str, action: str) -> bool:
        pass

    @abstractmethod
    def get_roles_for_user(self, user: str) -> List[str]:
        pass

    @abstractmethod
    def add_role_for_user(self, user: str, role: str) -> bool:
        pass
