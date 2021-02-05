import asyncio
import aiosqlite


class SQLite:
    def __init__(self, filename):
        self.filename = filename
        self.is_open = True

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    async def __aenter__(self):
        await self.wait_for_opening()
        self.close()

    async def __aexit__(self, *args, **kwargs):
        self.open()

    async def execute(self, query):
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute(query) as cursor:
                result = await cursor.fetchall()
                await db.commit()
                return result

    async def wait_for_opening(self):
        while not self.is_open:
            await asyncio.sleep(0.5)
