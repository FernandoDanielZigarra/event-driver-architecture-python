# tests/integration/users/test_create_user_use_case.py

import pytest
from app.modules.users.domain.models.models import UserCreateInput
from app.modules.users.application.use_cases.create_user import CreateUserUseCase
from app.modules.users.infrastructure.repositories.memory import InMemoryUserRepository
from app.core.events.event_bus import EventBus
from app.modules.users.domain.validations.user_validator import UserValidator


@pytest.mark.asyncio
async def test_create_user_successfully():
    input_data = UserCreateInput(
        username="newuser",
        email="new@example.com",
        first_name="Ana",
        last_name="Torres",
        raw_password="Password1!"
    )

    # Mocks simples
    repo = InMemoryUserRepository()
    event_bus = EventBus()

    class DummyUserValidator(UserValidator):
        async def validate_user_create_input(self, user_input):
            pass  # Validación dummy

    validator = DummyUserValidator(repo)

    # Caso de uso con todas las dependencias
    use_case = CreateUserUseCase(repo=repo, event_bus=event_bus, validator=validator)

    user = await use_case.execute(input_data)

    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "new@example.com"