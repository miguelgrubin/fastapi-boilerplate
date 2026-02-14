from fastapi import FastAPI, Response
from src.blog import USER_CREATOR, USER_DELETER
from src.blog.infrastructure.mappers.user_mapper import UserMapper
from src.blog.infrastructure.server.user_dtos import UserCreationDTO, UserResponse
from src.blog.types import BlogUseCasesType
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter


def blog_routes(app: FastAPI, use_cases: BlogUseCasesType) -> None:
    @app.post("/app/v1/blog/users", response_model=UserResponse)
    def create_user(payload: UserCreationDTO) -> UserResponse:
        use_case: UserCreator = use_cases.get(USER_CREATOR)
        user = use_case.execute(payload.username, payload.password, payload.email)
        return UserMapper.toDTO(user)

    @app.delete("/admin/v1/blog/users/{user_id}", status_code=204)
    def delete_user(user_id: str) -> Response:
        use_case: UserDeleter = use_cases.get(USER_DELETER)
        use_case.execute(user_id)
        return Response(status_code=204)
