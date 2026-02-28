from dataclasses import dataclass

from src.shared.domain.services.password_service import PasswordService
from src.shared.domain.services.sql_service import SqlService


@dataclass
class SharedServices:
    password_service: PasswordService
    sql_service: SqlService
