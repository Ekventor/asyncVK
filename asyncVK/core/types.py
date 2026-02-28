from typing import TypedDict, Optional, Any


class Forward(TypedDict):
    peer_id: int
    conversation_message_ids: list[int]


class Reply(TypedDict):
    text: str
    peer_id: int
    user_id: int
    object_id: int


class Action(TypedDict):
    type: str
    text: str
    object_id: str
    member_id: str


class EventParams(TypedDict):
    type: str
    text: str
    user_id: int
    peer_id: int
    post_id: int
    owner_id: int
    object_id: int
    reply: Optional[Reply]
    action: Optional[Action]
    payload: Optional[Any]
