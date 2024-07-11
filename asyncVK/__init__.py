import asyncio
import aiohttp
import traceback
import sys

from . import handlers
from .chain import Chain
from .core import VERSION, get_event_params


class Handler:
    on = handlers.Handlers


class Bot:
    def __init__(self, token: str, group_id: int):
        self.session = aiohttp.ClientSession()
        self.token = token
        self.group_id = group_id
        self.config = {}
        self.handlers = []
        self.users_in_chain = []
        self.chains = []
        self.bound_chains = []

    def handle(self, handler: handlers.Handler) -> handlers.Handler:
        self.handlers.append(handler)
        return handler

    def add_chain(self, chain: Chain) -> Chain:
        self.chains.append(chain)
        return chain

    async def run_polling(self) -> None:
        async with self.session.get("https://api.vk.com/method/groups.getLongPollServer",
                                    params=f"group_id={self.group_id}&access_token={self.token}&v={VERSION}") as response:
            config = await response.json()
            print(config)
            self.config = config["response"]
            self.config["server"] = self.config["server"].replace("https://", "")

            async with self.session.get("https://api.vk.com/method/groups.getLongPollSettings",
                                        params=f"group_id={self.group_id}&access_token={self.token}&v={VERSION}") as response:
                print(await response.json())

            while True:
                try:
                    async with self.session.get(f"https://%s?act=a_check&key=%s&ts=%s&wait=60&mode=2&version={VERSION}" % (
                               self.config["server"], self.config["key"], self.config["ts"])) as response:
                        event = await response.json()
                        updates = event["updates"]
                        if len(updates) == 0:
                            continue
                        print(updates)

                        self.config["ts"] = event["ts"]

                        asyncio.create_task(self.send_event(updates[0]))

                except:
                    sys.stderr.write(f"\n\n{traceback.format_exc()}\n\n")

    async def send_event(self, event: dict) -> None:
        event_type = event["type"]
        event_params = get_event_params(event, event_type)

        if event_params["user_id"] not in self.users_in_chain:
            for chain in self.chains:
                if chain.is_trigger(event_params):
                    self.bound_chains.append(chain.bind_chain(event_params["user_id"]))
                    self.users_in_chain.append(event_params["user_id"])
                    break

        active_chains = [chain for chain in self.bound_chains if chain.is_trigger(event_type, event_params["user_id"])]
        tasks = [asyncio.create_task(chain.new_event(self, event, event_params))
                 for chain in active_chains]

        for future in asyncio.as_completed(tasks):
            result = await future
            if not result[0]:
                self.bound_chains.remove(result[1])
                self.users_in_chain.remove(event_params["user_id"])

        active_handlers = [handler for handler in self.handlers if handler.is_trigger(event_params)]
        tasks = [asyncio.create_task(handler.new_event(self, event, event_params))
                 for handler in active_handlers]
        await asyncio.gather(*tasks)

    async def execute(self, method: str, **params) -> dict:
        url = f"https://api.vk.com/method/{method}"
        query = ""
        for key, value in params.items():
            if value is not None:
                query += f"{key}={value}&"
        query += f"access_token={self.token}&v={VERSION}"

        async with self.session.post(url, params=query) as response:
            return await response.json()


def run_polling(bot: Bot) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run_polling())
