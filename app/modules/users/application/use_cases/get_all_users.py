
from app.modules.users.domain.models.models import UserOutput
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.modules.users.application.services.user_service import UserService
from app.core.events.event_bus import EventBus

class GetAllUsersUseCase:
    def __init__(self, repo: IUserRepository, event_bus: EventBus):
        self.service = UserService(repo, event_bus, None)

    async def execute(self) -> list[UserOutput]:
        return await self.service.service_get_all_users()
