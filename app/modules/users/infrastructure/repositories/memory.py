from app.modules.users.domain.models.models import UserCreateInput, UserCreate, UserOutput
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from datetime import datetime
from uuid import uuid4


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: list[UserOutput] = []

    async def repository_create_user(self, user: UserCreate) -> UserOutput:
        now = datetime.now()
        new_user = UserOutput(
            id=uuid4(),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=now,
            updated_at=now,
        )
        self._users.append(new_user)
        return new_user

    async def repository_get_all_users(self) -> list[UserOutput]:
        return self._users.copy()
    
    async def find_by_email(self, email: str) -> UserOutput | None:
        for user in self._users:
            if user.email == email:
                return user
        return None
