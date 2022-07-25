from typing import List, Tuple
from copy import deepcopy
from .handlers import Handler


class BoundChain:
    def __init__(self, handlers: List[Handler], user_id: int):
        self.handlers = handlers
        self.user_id = user_id
        self.data = None

    def is_trigger(self, event_type: str, user_id: int) -> bool:
        return event_type == self.handlers[0].event_type and user_id == self.user_id

    async def new_event(self, token: str, event: dict, event_params: dict) -> Tuple:
        result = None

        handler = self.handlers.pop(0)
        if handler.is_trigger(event_params):
            self.data = await handler.new_event(token, event, event_params, self.data)
            result = True
        else:
            result = False

        if len(self.handlers) < 1:
            result = False

        return result, self


class Chain:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: Handler) -> Handler:
        self.handlers.append(handler)
        return handler

    def is_trigger(self, event_params: dict) -> bool:
        return self.handlers[0].is_trigger(event_params)

    def bind_chain(self, user_id: int) -> BoundChain:
        return BoundChain(deepcopy(self.handlers), user_id)
