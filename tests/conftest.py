# tests/conftest.py

import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import AsyncGenerator
from app.db.session import AsyncSessionLocal, Base, engine
from app.core.events.event_bus import EventBus
from app.modules.users.domain.validations.user_validator import UserValidator


# ✅ 1. Cargar el entorno de test antes de iniciar
os.environ["APP_ENV"] = "test"


# ✅ 2. Fixture para crear y limpiar las tablas (opcional)
@pytest.fixture(scope="session", autouse=True)
async def create_test_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        # Si querés borrar todo después de los tests
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# ✅ 3. Fixture para una sesión de base de datos real
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


# ✅ 4. EventBus fixture
@pytest.fixture
def event_bus():
    return EventBus()


# ✅ 5. DummyValidator que use la sesión real
@pytest.fixture
def dummy_validator(db_session):
    class Dummy(UserValidator):
        def __init__(self):
            self.session = db_session

        async def validate_user_create_input(self, user_input):
            # Aquí podrías llamar a alguna validación real si querés
            pass

    return Dummy()
