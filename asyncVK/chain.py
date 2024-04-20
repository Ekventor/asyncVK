from typing import List, Tuple, Any
from copy import deepcopy
from .handlers import Handler


class Reject:
    pass


class Reset:
    pass


class BoundChain:
    def __init__(self, primal_chain, handlers: List[Handler], user_id: int):
        self.primal_chain = primal_chain
        self.handlers = handlers
        self.user_id = user_id
        self.data = None

    def is_trigger(self, event_type: str, user_id: int) -> bool:
        return event_type == self.handlers[0].event_type and user_id == self.user_id

    async def new_event(self, token: str, event: dict, event_params: dict) -> Tuple:
        handler = self.handlers[0]
        if handler.is_trigger(event_params):
            data = await handler.new_event(token, event, event_params, self.data)
            if isinstance(data, Reject):
                return False, self
        else:
            return False, self

        if not isinstance(data, Reset):
            self.handlers.pop(0)
            self.data = data

        if len(self.handlers) < 1:
            return False, self

        return True, self


class Chain:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: Handler) -> Handler:
        self.handlers.append(handler)
        return handler

    def is_trigger(self, event_params: dict) -> bool:
        return self.handlers[0].is_trigger(event_params)

    def bind_chain(self, user_id: int) -> BoundChain:
        return BoundChain(self, deepcopy(self.handlers), user_id)
