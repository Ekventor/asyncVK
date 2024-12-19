from typing import Union, Callable
from abc import ABC, abstractmethod


class BaseCondition(ABC):
    @abstractmethod
    def new_event(self, event_params: dict) -> bool:
        pass


class Condition(BaseCondition):
    def __init__(self, command: str = None, contains_command: str = None, user_id: int = None,
                 peer_id: int = None, post_id: int = None, owner_id: int = None, functional_condition: Callable = None):
        self.command = command
        self.contains_command = contains_command
        self.user_id = user_id
        self.peer_id = peer_id
        self.post_id = post_id
        self.owner_id = owner_id
        self.functional_condition = functional_condition

    def new_event(self, event_params: dict) -> bool:
        text = event_params["text"]
        user_id = event_params["user_id"]
        peer_id = event_params["peer_id"]
        post_id = event_params["post_id"]
        owner_id = event_params["owner_id"]

        if (self.contains_command is not None and self.contains_command in text) or \
                (self.command is not None and self.command == text) or \
                (self.user_id is not None and self.user_id == user_id) or \
                (self.peer_id is not None and self.peer_id == peer_id) or \
                (self.post_id is not None and self.post_id == post_id) or \
                (self.owner_id is not None and self.owner_id == owner_id) or \
                (self.functional_condition is not None and self.functional_condition(event_params)):
            return True

        return False


class ActionCondition(BaseCondition):
    def __init__(self, action: str = None, command: str = None, member_id: int = None,
                 contains_command: str = None):
        self.action = action
        self.command = command
        self.contains_command = contains_command
        self.member_id = member_id

    def new_event(self, event_params: dict) -> bool:
        text = event_params["action"].get("text")
        member_id = event_params["action"].get("member_id")
        event_type = event_params["action"].get("type")
        print(self.action, event_type)

        if (self.action is not None and self.action == event_type) or \
           (self.contains_command is not None and self.contains_command in text) or \
           (self.command is not None and self.command == text) or \
           (self.member_id is not None and self.member_id == member_id):
            return True

        return False


class PayloadCondition(BaseCondition):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def new_event(self, event_params: dict) -> bool:
        payload = event_params["payload"]
        for arg, value in self.kwargs.items():
            if payload.get(arg) != value:
                return False

        return True


class And(BaseCondition):
    def __init__(self, *conditions: BaseCondition):
        self.conditions = conditions

    def new_event(self, event_params: dict) -> bool:
        if all(list(map(lambda condition: condition.new_event(event_params), self.conditions))):
            return True

        return False


class Or(BaseCondition):
    def __init__(self, *conditions: BaseCondition):
        self.conditions = conditions

    def new_event(self, event_params: dict) -> bool:
        if any(list(map(lambda condition: condition.new_event(event_params), self.conditions))):
            return True

        return False
