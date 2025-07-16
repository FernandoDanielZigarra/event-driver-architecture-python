from app.modules.users.domain.models.models import UserCreate, UserOutput
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.modules.users.domain.exceptions import UserAlreadyExistsException
from asyncpg.exceptions import UniqueViolationError
from app.db.db import db
from ..sql_loader import load_query


INSERT_USER = load_query("insert_user.sql")
GET_ALL_USERS = load_query("get_all_users.sql")
GET_USER_BY_EMAIL = load_query("get_user_by_email.sql")


class UserRepository(IUserRepository):
    async def find_by_email(self, email: str) -> UserOutput | None:
        rows = await db.fetch(GET_USER_BY_EMAIL, email)
        if not rows:
            return None
        return UserOutput(**dict(rows[0]))

    async def repository_create_user(self, user: UserCreate) -> UserOutput:

        row = await db.fetch(
            INSERT_USER,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.hashed_password
        )
        return UserOutput(**dict(row[0]))

    async def repository_get_all_users(self) -> list[UserOutput]:
        rows = await db.fetch(GET_ALL_USERS)
        return [UserOutput(**dict(row)) for row in rows] if rows else []
