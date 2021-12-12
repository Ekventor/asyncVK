import asyncio
import aiosqlite
from typing import Iterable, Any


class Synchronizer:
    def __init__(self):
        self.is_open = True

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    async def __aenter__(self):
        await self.wait_for_opening()
        self.close()

    async def __aexit__(self, *args, **kwargs):
        self.open()

    async def wait_for_opening(self) -> None:
        while not self.is_open:
            await asyncio.sleep(0.2)


class SQLite(Synchronizer):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    async def execute(self, query: str, parameters: Iterable[Any] = None):
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute(query, parameters) as cursor:
                result = await cursor.fetchall()
                await db.commit()
                return result


class Variable(Synchronizer):
    def __init__(self, value):
        super().__init__()
        self.object = value
