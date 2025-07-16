import pytest
from app.modules.users.domain.models.models import UserCreateInput
from app.modules.users.domain.validations.user_validator import UserValidator
from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.modules.users.domain.exceptions import WeakPasswordException, UserAlreadyExistsException


# Datos válidos
valid_user = UserCreateInput(
    username="user123",
    email="user@example.com",
    first_name="Juan",
    last_name="Pérez",
    raw_password="Secure1!"
)

# Datos con contraseña débil
weak_password_user = UserCreateInput(
    username="user123",
    email="user@example.com",
    first_name="Juan",
    last_name="Pérez",
    raw_password="abc"
)

# Datos con email duplicado
existing_email_user = UserCreateInput(
    username="user123",
    email="existing@example.com",
    first_name="Juan",
    last_name="Pérez",
    raw_password="Secure1!"
)


# Mock básico pero completo de IUserRepository
class DummyUserRepository(IUserRepository):
    async def find_by_email(self, email: str):
        return None 

    async def repository_create_user(self, user):
        return UserCreateInput(**user.model_dump())
    async def repository_get_all_users(self):
        return []  # Simulamos lista vacía


# Mock para email existente
class ExistingEmailRepository(IUserRepository):
    async def find_by_email(self, email: str):
        return True  # Email ya existe

    async def repository_create_user(self, user):
        return UserCreateInput(**user.model_dump())

    async def repository_get_all_users(self):
        return []


# Mock para validación sin email existente
class WeakPasswordRepository(IUserRepository):
    async def find_by_email(self, email: str):
        return None

    async def repository_create_user(self, user):
        return UserCreateInput(**user.model_dump())

    async def repository_get_all_users(self):
        return []


# Fixtures
@pytest.fixture
def validator():
    return UserValidator(DummyUserRepository())

@pytest.fixture
def validator_with_existing_email():
    return UserValidator(ExistingEmailRepository())

@pytest.fixture
def validator_with_weak_password():
    return UserValidator(WeakPasswordRepository())