from typing import Dict, List, Optional, Tuple

import json

from sqlalchemy import delete, insert, select
from src.blog.domain.user import Profile, User
from src.blog.domain.user_repository import UserRepository
from src.blog.infrastructure.storage.sql_tables import users_table
from src.shared.domain.services.sql_service import SqlService


class UserRepositorySql(UserRepository):
    def __init__(self, sql_service: SqlService) -> None:
        self._sql_service = sql_service

    def save(self, user: User) -> None:
        with self._sql_service.session() as conn:
            # Check if user already exists (upsert logic)
            existing = conn.execute(
                select(users_table).where(users_table.c.id == user.id)
            ).fetchone()

            if existing:
                conn.execute(
                    users_table.update()
                    .where(users_table.c.id == user.id)
                    .values(**self._to_row(user))
                )
            else:
                conn.execute(insert(users_table).values(**self._to_row(user)))

    def delete(self, user_id: str) -> None:
        with self._sql_service.session() as conn:
            conn.execute(delete(users_table).where(users_table.c.id == user_id))

    def find_one(self, user_id: str) -> Optional[User]:
        with self._sql_service.session() as conn:
            row = conn.execute(select(users_table).where(users_table.c.id == user_id)).fetchone()
            return self._to_entity(row) if row else None

    def find_one_by_username(self, username: str) -> Optional[User]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(users_table).where(users_table.c.username == username)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_one_by_email(self, email: str) -> Optional[User]:
        with self._sql_service.session() as conn:
            row = conn.execute(select(users_table).where(users_table.c.email == email)).fetchone()
            return self._to_entity(row) if row else None

    def find_all(
        self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
    ) -> List[User]:
        with self._sql_service.session() as conn:
            query = select(users_table)

            offset, limit = find_limits
            query = query.offset(offset).limit(limit)

            rows = conn.execute(query).fetchall()
            return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_row(user: User) -> dict:
        """Map a domain User entity to a database row dictionary."""
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "bio": user.profile.bio,
            "image": user.profile.image,
            "following": json.dumps(user.following),
            "followers": json.dumps(user.followers),
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def _to_entity(row) -> User:  # type: ignore[no-untyped-def]
        """Map a database row to a domain User entity."""
        following = row.following
        if isinstance(following, str):
            following = json.loads(following)

        followers = row.followers
        if isinstance(followers, str):
            followers = json.loads(followers)

        return User(
            id=row.id,
            email=row.email,
            username=row.username,
            password_hash=row.password_hash,
            profile=Profile(
                bio=row.bio,
                image=row.image,
            ),
            following=following or [],
            followers=followers or [],
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
