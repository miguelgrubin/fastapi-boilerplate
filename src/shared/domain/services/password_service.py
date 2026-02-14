from abc import ABC, abstractmethod

PASSWORD_SERVICE = "PasswordService"


class PasswordService(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def check(self, password: str, password_hash: str) -> bool:
        pass
