from typing import List, NoReturn, Optional

from copy import copy

from src.app.blog.domain.user import User
from src.app.blog.domain.user_repository import UserRepository


class UserRepositoryMemory(UserRepository):
    _users: List[User] = []

    def save(self, user: User) -> User:
        self._users.append(user)

    def delete(self, user_id: str) -> NoReturn:
        if user := self.find_one(user_id):
            self._users.remove(user)

    def find_one(self, user_id: str) -> Optional[User]:
        return next(filter(lambda x: x.id == user_id, self._users), None)

    def find_one_by_email_or_username(self, email: str, username: str) -> Optional[User]:
        return next(filter(lambda x: x.email == email or x.username == username, self._users), None)

    def find_all(self) -> List[User]:
        filtered_users = copy(self._users)
        return filtered_users

    def clear(self):
        self._users = []
