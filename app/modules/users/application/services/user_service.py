from app.modules.users.domain.models.models import UserCreate, UserOutput, UserCreateInput
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.utils.bcrypt import hash_password
from app.modules.users.domain.events.events import UserCreatedEvent
from app.core.events.event_bus import EventBus
from app.modules.users.domain.validations.user_validator import UserValidator


class UserService:
    def __init__(
        self,
        repo: IUserRepository,
        event_bus: EventBus,
        validator: UserValidator | None = None
    ):
        self.repo = repo
        self.event_bus = event_bus
        self.validator = validator

    async def service_create_user(self, user: UserCreateInput):
        if self.validator:
            await self.validator.validate_user_create_input(user)

        hashed_password = hash_password(user.raw_password)

        user_data = UserCreate(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=hashed_password,
        )

        new_user: UserOutput = await self.repo.repository_create_user(user_data)

        await self.event_bus.publish(UserCreatedEvent(id=new_user.id, email=new_user.email))

        return new_user

    async def service_get_all_users(self) -> list[UserOutput]:
        return await self.repo.repository_get_all_users()
