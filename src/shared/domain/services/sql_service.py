from typing import Any, Iterator

from abc import ABC, abstractmethod
from contextlib import contextmanager

SQL_SERVICE = "SqlService"


class SqlService(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Create the database engine and initialize the connection pool."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Dispose of the engine and release all connections."""
        pass

    @abstractmethod
    @contextmanager
    def session(self) -> Iterator[Any]:
        """Context manager that yields a database connection with transaction management.

        Usage:
            with sql_service.session() as connection:
                connection.execute(...)

        Commits on success, rolls back on exception.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Any:
        """Return the SQLAlchemy MetaData object for migration tooling."""
        pass
