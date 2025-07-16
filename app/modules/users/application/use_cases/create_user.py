from app.modules.users.domain.models.models import UserCreateInput, UserOutput
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.modules.users.application.services.user_service import UserService
from app.core.events.event_bus import EventBus
from app.modules.users.domain.validations.user_validator import UserValidator


class CreateUserUseCase:
    def __init__(
        self,
        repo: IUserRepository,
        event_bus: EventBus,
        validator: UserValidator
    ):
        self.service = UserService(
            repo=repo,
            event_bus=event_bus,
            validator=validator
        )

    async def execute(self, user: UserCreateInput) -> UserOutput:
        return await self.service.service_create_user(user)