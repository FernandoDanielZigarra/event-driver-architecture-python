from abc import ABC, abstractmethod
from app.modules.users.domain.models.models import UserCreate, UserOutput

class IUserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> UserOutput | None: ...
    
    @abstractmethod
    async def repository_create_user(self, user: UserCreate) -> UserOutput: ...

    @abstractmethod
    async def repository_get_all_users(self) -> list[UserOutput]: ...



