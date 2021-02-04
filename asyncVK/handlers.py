from typing import Union

import asyncio
import aiohttp

from .dispatcher import Dispatcher
from .condition import Condition, And, Or


class Handler:
    def __init__(self, condition: Union[Condition, And, Or] = None, is_lower: bool = False, func=None):
        self.condition = condition
        self.is_lower = is_lower
        self.func = func
        self.is_ready = True

    def __call__(self, func):
        async def wrapper(event: dict, token: str, text: str = None, user_id: int = None, peer_id: int = None, owner_id: int = None, post_id: int = None):
            await func(Dispatcher(event, token, text, user_id, peer_id=peer_id, post_id=post_id, owner_id=owner_id))

        return type(self)(self.condition, self.is_lower, wrapper)


class CustomHandler(Handler):
    def __call__(self, func):
        async def wrapper(event: dict, token: str, text: str = None, user_id: int = None, peer_id: int = None, owner_id: int = None, post_id: int = None):
            await func(Dispatcher(event, token, text, user_id, peer_id=peer_id, post_id=post_id, owner_id=owner_id))

        handler = CustomHandler(self.condition, self.is_lower, wrapper)
        handler.event_type = self.event_type
        return handler

    async def new_event(self, token: str, event: dict) -> None:
        if "message" in event["object"]:
            text = event["object"]["message"]["text"]
            user_id = event["object"]["message"]["from_id"]
            peer_id = event["object"]["message"]["peer_id"]
            post_id = None
            owner_id = None
        else:
            text = event["object"]["text"]
            user_id = event["object"]["from_id"]
            peer_id = event["object"].get("peer_id")
            post_id = event["object"].get("post_id")
            owner_id = event["object"].get("owner_id")

        while True:
            if self.is_ready:
                self.is_ready = False
                await self.func(event, token, text, user_id, peer_id=peer_id, owner_id=owner_id, post_id=post_id)
                self.is_ready = True
                break
            else:
                await asyncio.sleep(0.5)


class MessageNewHandler(Handler):
    event_type = "message_new"

    async def new_event(self, token: str, event: dict) -> None:
        try:
            text = event["object"]["message"]["text"] if not self.is_lower else event["object"]["message"]["text"].lower()
            peer_id = event["object"]["message"]["peer_id"]
            user_id = event["object"]["message"]["from_id"]

            if self.condition.new_event(text=text, user_id=user_id, peer_id=peer_id):
                while True:
                    if self.is_ready:
                        self.is_ready = False
                        await self.func(event, token, text, user_id, peer_id=peer_id)
                        self.is_ready = True
                        break
                    else:
                        await asyncio.sleep(0.5)

        except (IndexError, KeyError):
            pass


class MessageEditHandler(Handler):
    event_type = "message_edit"

    async def new_event(self, token: str, event: dict) -> None:
        try:
            text = event["object"]["text"] if not self.is_lower else event["object"]["text"].lower()
            peer_id = event["object"]["peer_id"]
            user_id = event["object"]["from_id"]

            if self.condition.new_event(text=text, user_id=user_id, peer_id=peer_id):
                while True:
                    if self.is_ready:
                        self.is_ready = False
                        await self.func(event, token, text, user_id, peer_id=peer_id)
                        self.is_ready = True
                        break
                    else:
                        await asyncio.sleep(0.5)

        except (IndexError, KeyError):
            pass


class WallReplyNewHandler(Handler):
    event_type = "wall_reply_new"

    async def new_event(self, token: str, event: dict) -> None:
        try:
            text = event["object"]["text"] if not self.is_lower else event["object"]["text"].lower()
            owner_id = event["object"]["owner_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["post_id"]

            if self.condition.new_event(text=text, user_id=user_id, post_id=post_id, owner_id=owner_id):
                while True:
                    if self.is_ready:
                        self.is_ready = False
                        await self.func(event, token, text, user_id, owner_id=owner_id, post_id=post_id)
                        self.is_ready = True
                        break
                    else:
                        await asyncio.sleep(0.5)

        except (IndexError, KeyError):
            pass


class WallReplyEditHandler(WallReplyNewHandler):
    event_type = "wall_reply_edit"


class WallPostNewHandler(Handler):
    event_type = "wall_post_new"

    async def new_event(self, token: str, event: dict) -> None:
        try:
            text = event["object"]["text"] if not self.is_lower else event["object"]["text"].lower()
            owner_id = event["object"]["owner_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["id"]

            if self.condition.new_event(text=text, user_id=user_id, post_id=post_id, owner_id=owner_id):
                while True:
                    if self.is_ready:
                        self.is_ready = False
                        await self.func(event, token, text, user_id, owner_id=owner_id, post_id=post_id)
                        self.is_ready = True
                        break
                    else:
                        await asyncio.sleep(0.5)

        except (IndexError, KeyError):
            pass


class BoardPostNewHandler(Handler):
    event_type = "board_post_new"

    async def new_event(self, token: str, event: dict) -> None:
        try:
            text = event["object"]["text"] if not self.is_lower else event["object"]["text"].lower()
            owner_id = event["group_id"]
            user_id = event["object"]["from_id"]
            post_id = event["object"]["topic_id"]

            if self.condition.new_event(text=text, user_id=user_id, post_id=post_id, owner_id=owner_id):
                while True:
                    if self.is_ready:
                        self.is_ready = False
                        await self.func(event, token, text, user_id, owner_id=owner_id, post_id=post_id)
                        self.is_ready = True
                        break
                    else:
                        await asyncio.sleep(0.5)

        except (IndexError, KeyError):
            pass


class BoardPostEditHandler(BoardPostNewHandler):
    event_type = "board_post_edit"


class Handlers:
    message_new = MessageNewHandler
    message_edit = MessageEditHandler
    wall_reply_new = WallReplyNewHandler
    wall_reply_edit = WallReplyEditHandler
    wall_post_new = WallPostNewHandler
    board_post_new = BoardPostNewHandler
    board_post_edit = BoardPostEditHandler

    def __new__(cls, event_type):
        handler = CustomHandler()
        handler.event_type = event_type
        return handler
