import asyncio


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
