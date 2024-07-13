from typing import Union, Any
import traceback
import sys

from .dispatcher import get_dispatcher_by_event
from .condition import Condition, ActionCondition, PayloadCondition, And, Or


class Handler:
    event_type = None

    def __init__(self, condition: Union[Condition, ActionCondition, PayloadCondition, And, Or] = None,
                 is_lower: bool = False, func=None):
        self.condition = condition
        self.is_lower = is_lower
        self.func = func

    def __call__(self, func):
        async def wrapper(bot, event: dict, event_params: dict, chain_data: Any):
            return await func(get_dispatcher_by_event(bot, event, event_params, chain_data))

        return type(self)(self.condition, self.is_lower, wrapper)

    def is_trigger(self, event_params: dict) -> bool:
        if event_params["type"] != self.event_type:
            return False

        if self.is_lower:
            if event_params["text"]:
                event_params["text"] = event_params["text"].lower()
            if "text" in event_params["action"]:
                event_params["action"]["text"] = event_params["action"]["text"].lower()
            if "text" in event_params["reply"]:
                event_params["reply"]["text"] = event_params["reply"]["text"].lower()

        return self.condition is None or self.condition.new_event(event_params)

    async def new_event(self, bot, event: dict, event_params: dict, chain_data: Any = None) -> Any:
        try:
            return await self.func(bot, event, event_params, chain_data)
        except:
            sys.stderr.write(f"\n\n{traceback.format_exc()}\n\n")


class CustomHandler(Handler):
    def __call__(self, func):
        async def wrapper(token: str, event: dict, event_params: dict, chain_data: Any):
            await func(get_dispatcher_by_event(token, event, event_params, chain_data))

        handler = CustomHandler(self.condition, self.is_lower, wrapper)
        handler.event_type = self.event_type
        return handler


class MessageNewHandler(Handler):
    event_type = "message_new"


class MessageEditHandler(Handler):
    event_type = "message_edit"


class WallReplyNewHandler(Handler):
    event_type = "wall_reply_new"


class WallReplyEditHandler(Handler):
    event_type = "wall_reply_edit"


class WallPostNewHandler(Handler):
    event_type = "wall_post_new"


class BoardPostNewHandler(Handler):
    event_type = "board_post_new"


class BoardPostEditHandler(Handler):
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
