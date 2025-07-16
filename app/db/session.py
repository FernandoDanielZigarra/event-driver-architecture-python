from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.db.config import settings

# Crear el engine a partir de la URL dinámica
engine = create_async_engine(settings.database_url, echo=False)

# Crear una fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base declarativa para modelos
Base = declarative_base()
