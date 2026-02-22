from dataclasses import dataclass

from src.shared.domain.services.password_service import PasswordService


@dataclass
class SharedServices:
    password_service: PasswordService
