from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.domain.user_repository import UserRepository
from src.shared.use_cases.use_case import UseCase


class UserDeleter(UseCase):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, user_id: str) -> None:
        user = self.user_repository.find_one(user_id)
        if not user:
            raise UserNotFound(user_id)
        self.user_repository.delete(user_id)
