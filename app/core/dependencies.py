from fastapi import Depends
from app.modules.users.infrastructure.repositories.user_repository import UserRepository
from app.core.events.event_bus import event_bus
from app.modules.users.domain.validations.user_validator import UserValidator
from app.modules.users.domain.interfaces.user_repository import IUserRepository

def get_user_repo():
    return UserRepository()

def get_event_bus():
    return event_bus

def get_validator(repo: IUserRepository = Depends(get_user_repo)):
    return UserValidator(repo)