from blog.domain.errors.username_already_exists import UserAlreadyExists
from src.blog.domain.user import User
from src.blog.domain.user_repository import UserRepository
from src.shared.domain.services.password_service import PasswordService
from src.shared.use_cases.use_case import UseCase


class UserCreator(UseCase):
    def __init__(self, user_repository: UserRepository, password_service: PasswordService) -> None:
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(self, username: str, password: str, email: str) -> User:
        recorded = self.user_repository.find_one_by_email(email)
        if recorded:
            raise UserAlreadyExists("Email already exists.")
        recorded = self.user_repository.find_one_by_username(username)
        if recorded:
            raise UserAlreadyExists("Username already exists.")
        password_hash = self.password_service.hash(password)
        user = User.create(username, password_hash, email)
        self.user_repository.save(user)
        return user
