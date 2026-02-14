from typing import List, NoReturn, Optional

from abc import ABC, abstractmethod

from src.blog.domain.user import User

USER_REPOSITORY = "UserRepository"


class UserRepository(ABC):
    """docstring for UserRepository"""

    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def find_one_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_one_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, find_filters, find_order, find_limits) -> List[User]:
        raise NotImplementedError
