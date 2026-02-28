from typing import Iterator

from contextlib import contextmanager

from sqlalchemy import Connection, Engine, MetaData, create_engine
from src.shared.domain.services.sql_service import SqlService


class SqlServiceSqlAlchemy(SqlService):
    def __init__(self, database_url: str, metadata: MetaData) -> None:
        self._database_url = database_url
        self._metadata = metadata
        self._engine: Engine | None = None

    def connect(self) -> None:
        self._engine = create_engine(self._database_url, echo=False)

    def disconnect(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

    @contextmanager
    def session(self) -> Iterator[Connection]:
        if self._engine is None:
            raise RuntimeError("SqlService is not connected. Call connect() first.")

        with self._engine.connect() as connection:
            try:
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    def get_metadata(self) -> MetaData:
        return self._metadata
