from src.blog.domain.user import User
from src.blog.infrastructure.server.user_dtos import ProfileResponse, UserResponse


class UserMapper:
    @staticmethod
    def toDTO(user: User) -> UserResponse:
        user_profile = ProfileResponse(bio=user.profile.bio, image=user.profile.image)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            profile=user_profile,
            created_at=user.created_at,
            updated_at=user.updated_at,
            followers=user.followers,
            following=user.following,
        )
