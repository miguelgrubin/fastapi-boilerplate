from src.shared.domain.services.password_service import PasswordService


class PasswordServiceFake(PasswordService):
    def hash(self, password: str) -> str:
        return password

    def check(self, password: str, password_hash: str) -> bool:
        return password == password_hash
