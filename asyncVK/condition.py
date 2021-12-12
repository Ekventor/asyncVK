from typing import Union


class Condition:
    def __init__(self, command: str = None, contains_command: str = None,
                 user_id: int = None, peer_id: int = None, post_id: int = None, owner_id: int = None):
        self.command = command
        self.contains_command = contains_command
        self.user_id = user_id
        self.peer_id = peer_id
        self.post_id = post_id
        self.owner_id = owner_id

    def new_event(self, text: str = None, user_id: int = None, peer_id: int = None, post_id: int = None, owner_id: int = None) -> bool:
        if (self.contains_command is not None and self.contains_command in text) or \
                (self.command is not None and self.command == text) or \
                (self.user_id is not None and self.user_id == user_id) or \
                (self.peer_id is not None and self.peer_id == peer_id) or \
                (self.post_id is not None and self.post_id == post_id) or \
                (self.owner_id is not None and self.owner_id == owner_id):
            return True

        return False


class And:
    def __init__(self, *conditions: Union[Condition, "And", "Or"]):
        self.conditions = conditions

    def new_event(self, text: str = None, user_id: int = None, peer_id: int = None, post_id: int = None, owner_id: int = None) -> bool:
        if all(list(map(lambda condition: condition.new_event(text, user_id, peer_id), self.conditions))):
            return True

        return False


class Or:
    def __init__(self, *conditions: Union[Condition, And, "Or"]):
        self.conditions = conditions

    def new_event(self, text: str = None, user_id: int = None, peer_id: int = None, post_id: int = None, owner_id: int = None) -> bool:
        if any(list(map(lambda condition: condition.new_event(text, user_id, peer_id), self.conditions))):
            return True

        return False
