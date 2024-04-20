import asyncio
import aiosqlite

from typing import Iterable, Any


class Synchronizer:
    def __init__(self):
        self.queue = []

    async def __aenter__(self):
        event = asyncio.Event()
        self.queue.append(event)
        await self.wait_for_opening()

    async def __aexit__(self, *args, **kwargs):
        if len(self.queue) > 1:
            event = self.queue.pop(1)
            event.set()
        else:
            self.queue.pop(0)

    async def wait_for_opening(self) -> None:
        if len(self.queue) < 2:
            return

        await self.queue[-1].wait()


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
