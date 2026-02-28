from sqlalchemy import MetaData

from src.shared.domain.services.password_service import PasswordService
from src.shared.domain.services.sql_service import SqlService
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
