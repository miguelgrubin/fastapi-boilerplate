from passlib.hash import argon2

from app.shared.services.domain.password_service import PasswordService


class PasswordServiceArgon(PasswordService):
    def hash(self, password: str) -> str:
        return argon2.hash(password)

    def check(self, password: str, password_hash: str) -> bool:
        return argon2.verify(password, password_hash)
