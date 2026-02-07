from typing import List, NoReturn, Optional

from abc import ABC, abstractmethod

from src.app.blog.domain.user import User


class UserRepository(ABC):
    """docstring for UserRepository"""

    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def find_one_by_email_or_username(self, email: str, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, find_filters, find_order, find_limits) -> List[User]:
        raise NotImplementedError
