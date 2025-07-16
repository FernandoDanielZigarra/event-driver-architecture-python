from fastapi import APIRouter
from app.modules.users.domain.models.models import UserOutput, UserCreateInput
from app.modules.users.infrastructure.repositories.user_repository import UserRepository
from app.modules.users.application.use_cases.get_all_users import GetAllUsersUseCase
from app.modules.users.application.use_cases.create_user import CreateUserUseCase
from app.core.response import ResponseModel, success_response, error_response
from app.core.pagination import PaginationMeta
from fastapi import Depends
from app.core.dependencies import get_user_repo, get_event_bus
from app.modules.users.domain.validations.user_validator import UserValidator
from app.core.dependencies import get_validator

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def api_get_all_users(
    repo: UserRepository = Depends(get_user_repo),
    event_bus = Depends(get_event_bus)
):
    use_case = GetAllUsersUseCase(repo=repo, event_bus=event_bus)
    users = await use_case.execute()
    meta = PaginationMeta(page=1, per_page=10, total=100)
    return success_response("Usuarios obtenidos correctamente", users, meta)


@router.post("/", response_model=ResponseModel[UserOutput, None, dict])
async def create_user_api(
    user: UserCreateInput,
    repo: UserRepository = Depends(get_user_repo),
    event_bus = Depends(get_event_bus),
    validator: UserValidator = Depends(get_validator)
):
    try:
        use_case = CreateUserUseCase(
            repo=repo,
            event_bus=event_bus,
            validator=validator
        )
        result = await use_case.execute(user)
        return success_response("Usuario creado", result)
    except Exception as e:
        return error_response(
            "No se pudo crear el usuario",
            error={"type": type(e).__name__, "detail": str(e)}
        )