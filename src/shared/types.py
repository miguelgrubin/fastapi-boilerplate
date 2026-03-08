from dataclasses import dataclass

from src.shared.domain.services.authentication_service import AuthenticationService
from src.shared.domain.services.authorization_service import AuthorizationService
from src.shared.domain.services.password_service import PasswordService
from src.shared.domain.services.sql_service import SqlService


@dataclass
class SharedServices:
    password_service: PasswordService
    sql_service: SqlService
    authentication_service: AuthenticationService
    authorization_service: AuthorizationService
