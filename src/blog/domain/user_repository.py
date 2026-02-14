from typing import Dict, List, Optional, Tuple

from abc import ABC, abstractmethod

from src.blog.domain.user import User


class UserRepository(ABC):
    """docstring for UserRepository"""

    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
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
    def find_all(
        self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
    ) -> List[User]:
        raise NotImplementedError
