import os
from typing import Optional
import asyncpg
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self._dsn: Optional[str] = None

    async def connect(self):
        dsn = os.getenv("DATABASE_URL", "")
        dsn_asyncpg = dsn.replace("postgresql+asyncpg://", "postgresql://")
        self._dsn = dsn_asyncpg
        self.pool = await asyncpg.create_pool(dsn_asyncpg, min_size=1, max_size=10)

    async def disconnect(self):
        if self.pool:
            try:
                await self.pool.close()
            except Exception:
                pass

    async def get_tables(self) -> list[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
            )
            return [dict(row) for row in rows]

    async def get_table_schema(self, table_name: str) -> list[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = $1
                ORDER BY ordinal_position
            """,
                table_name,
            )
            return [dict(row) for row in rows]

    async def execute_query(self, query: str) -> list[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]

    async def execute_insert(self, query: str, *args) -> str:
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, *args)
            return result


db = DatabaseManager()
