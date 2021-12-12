import asyncio
import aiohttp
import traceback
import sys

from .handlers import Handlers
from .dispatcher import Dispatcher, get_dispatcher_by_event


class Handler:
    on = Handlers


class Bot:
    def __init__(self, token: str, group_id: int):
        self.token = token
        self.group_id = group_id
        self.config = {}
        self.handlers = []
        self.middlewares = []
        self.is_rejected = False

    def handle(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)

    def reject(self):
        self.is_rejected = True

    async def run_polling(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.vk.com/method/groups.getLongPollServer",
                                   params=f"group_id={self.group_id}&access_token={self.token}&v=5.126") as response:
                config = await response.json()
                print(config)
                self.config = config["response"]
                self.config["server"] = self.config["server"].replace("https://", "")

                async with session.get("https://api.vk.com/method/groups.getLongPollSettings",
                                       params=f"group_id={self.group_id}&access_token={self.token}&v=5.126") as response:
                    print(await response.json())

                while True:
                    try:
                        async with session.get("https://%s?act=a_check&key=%s&ts=%s&wait=60&mode=2&version=5.126" % (self.config["server"], self.config["key"], self.config["ts"])) as response:
                            event = await response.json()
                            updates = event["updates"]
                            if len(updates) == 0:
                                continue
                            print(updates)

                            self.config["ts"] = event["ts"]

                            asyncio.create_task(self.send_event(updates[0]))

                    except:
                        sys.stderr.write(f"\n\n{traceback.format_exc()}\n\n")

    async def send_event(self, event):
        tasks = [asyncio.create_task(middleware.pre(get_dispatcher_by_event(event, event["type"], self.token), self.reject))
                 for middleware in self.middlewares if middleware.event_type in (event["type"], None)]
        await asyncio.gather(*tasks)

        if self.is_rejected:
            self.is_rejected = False
            return

        tasks = [asyncio.create_task(handler.new_event(self.token, event))
                 for handler in self.handlers if handler.event_type == event["type"]]
        await asyncio.gather(*tasks)

        tasks = [asyncio.create_task(middleware.post(get_dispatcher_by_event(event, event["type"], self.token)))
                 for middleware in self.middlewares if middleware.event_type in (event["type"], None)]
        await asyncio.gather(*tasks)

    async def execute(self, method: str, **params) -> dict:
        query = f"https://api.vk.com/method/{method}?"
        for key, value in params.items():
            query += f"{key}={value}&"
        query += f"access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            async with session.get(query) as response:
                return await response.json()


def run_polling(bot: Bot) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run_polling())
