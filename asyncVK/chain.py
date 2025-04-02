from typing import Callable, Optional, Any
from dataclasses import dataclass
from .handlers import Handler

from .core.types import EventParams


@dataclass
class ChainResult:
    to: Optional[str]
    data: Any = None


class BoundChain:
    def __init__(self, handlers: dict[str, Handler], current_handler: str, user_id: int):
        self.handlers = handlers
        self.current_handler = current_handler
        self.user_id = user_id
        self.data = None

    def is_trigger(self, event_type: str, user_id: int) -> bool:
        return event_type == self.handlers[self.current_handler].event_type and user_id == self.user_id

    async def new_event(self, bot, event: dict, event_params: EventParams) -> tuple[bool, "BoundChain"]:
        handler = self.handlers[self.current_handler]
        if not handler.is_trigger(event_params):
            return False, self

        chain_result: Optional[ChainResult] = await handler.new_event(bot, event, event_params, self.data)
        if chain_result is None:
            return False, self
        if chain_result.to is None:
            return False, self

        self.current_handler = chain_result.to
        self.data = chain_result.data

        return True, self


class Chain:
    def __init__(self):
        self.initial_handler: Optional[Handler] = None
        self.initial_handler_name: Optional[str] = None
        self.handlers: dict[str, Handler] = dict()

    def add_handler(self, handler_name: str) -> Callable:
        def decorator(handler: Handler) -> Handler:
            if self.initial_handler is None:
                self.initial_handler = handler
                self.initial_handler_name = handler_name

            self.handlers[handler_name] = handler
            return handler

        return decorator

    def is_trigger(self, event_params: EventParams) -> bool:
        if self.initial_handler is None:
            return False

        return self.initial_handler.is_trigger(event_params)

    def bind_chain(self, user_id: int) -> BoundChain:
        return BoundChain(self.handlers, self.initial_handler_name, user_id)
