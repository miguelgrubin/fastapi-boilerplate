from sqlalchemy import MetaData

from src.shared.domain.services.authentication_service import AuthenticationService
from src.shared.domain.services.authorization_service import AuthorizationService
from src.shared.domain.services.password_service import PasswordService
from src.shared.domain.services.sql_service import SqlService
from src.shared.infrastructure.services.authentication_service_authlib import (
    AuthenticationServiceAuthlib,
)
from src.shared.infrastructure.services.authentication_service_fake import (
    AuthenticationServiceFake,
)
from src.shared.infrastructure.services.authorization_service_casbin import (
    AuthorizationServiceCasbin,
)
from src.shared.infrastructure.services.authorization_service_fake import AuthorizationServiceFake
from src.shared.infrastructure.services.password_service_argon import PasswordServiceArgon
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake
from src.shared.infrastructure.services.sql_service_sqlalchemy import SqlServiceSqlAlchemy


def create_password_service(keyword: str) -> PasswordService:
    if keyword == "argon2":
        return PasswordServiceArgon()
    return PasswordServiceFake()


def create_sql_service(database_url: str, metadata: MetaData) -> SqlService:
    service = SqlServiceSqlAlchemy(database_url, metadata)
    service.connect()
    return service


def create_authentication_service(
    client_id: str,
    client_secret: str,
    issuer_url: str,
    verify_ssl: bool = True,
) -> AuthenticationService:
    if client_id and client_secret and issuer_url:
        return AuthenticationServiceAuthlib(
            client_id=client_id,
            client_secret=client_secret,
            issuer_url=issuer_url,
            verify_ssl=verify_ssl,
        )
    return AuthenticationServiceFake()


def create_authorization_service(
    model_path: str,
    policy_path: str,
) -> AuthorizationService:
    if model_path and policy_path:
        return AuthorizationServiceCasbin(
            model_path=model_path,
            policy_path=policy_path,
        )
    return AuthorizationServiceFake()
