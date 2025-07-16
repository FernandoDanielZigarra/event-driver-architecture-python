import asyncpg
import logging
from app.db.config import settings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=settings.database_user,
                password=settings.database_password,
                database=settings.database_name,
                host=settings.database_host,
                port=settings.database_port,
                min_size=1,
                max_size=5
            )
            logger.info("Conexión a la BD establecida")
        except Exception as e:
            logger.error(f"Error conectando a la BD: {e}")
            raise

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Conexión a la BD cerrada")

    async def fetch(self, query: str, *args):
        if not self.pool:
            raise RuntimeError("Pool no inicializado")
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(query, *args)
        except Exception as e:
            logger.error(f"Error ejecutando query: {e}")
            raise

    async def execute(self, query: str, *args):
        if not self.pool:
            raise RuntimeError("Pool no inicializado")
        try:
            async with self.pool.acquire() as conn:
                return await conn.execute(query, *args)
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            raise


db = Database()
