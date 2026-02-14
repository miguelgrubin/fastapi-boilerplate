from pwdlib import PasswordHash
from src.shared.domain.services.password_service import PasswordService


class PasswordServiceArgon(PasswordService):
    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def check(self, password: str, password_hash: str) -> bool:
        return self._password_hash.verify(password, password_hash)
