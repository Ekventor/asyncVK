from typing import Any, Union
import json

from .core.message import Message, MessageTemplate
from .core.keyboard import Keyboard
from .core.types import EventParams, Forward


class Dispatcher:
    def __init__(self, event: dict, event_type: str, bot, text: str = None, user_id: int = None, peer_id: int = None,
                 post_id: int = None, owner_id: int = None, object_id: int = None, reply_text: str = None,
                 reply_user_id: int = None, reply_peer_id: int = None, reply_object_id: int = None,
                 action_type: str = None, action_text: str = None, action_object_id: int = None,
                 action_member_id: int = None, payload: Any = None, chain_data: Any = None):
        self.event_type = event_type
        self.bot = bot
        self.user_id = user_id
        self.peer_id = peer_id
        self.chat_id = peer_id - 2000000000
        self.post_id = post_id
        self.owner_id = owner_id
        self.object_id = object_id
        self.event = event
        self.text = text
        self.reply_text = reply_text
        self.reply_user_id = reply_user_id
        self.reply_peer_id = reply_peer_id
        self.reply_object_id = reply_object_id
        self.action_type = action_type
        self.action_text = action_text
        self.action_object_id = action_object_id
        self.action_member_id = action_member_id
        self.payload = payload
        self.chain_data = chain_data

    @property
    def message(self) -> Message:
        return Message(self.bot, self.peer_id, self.object_id)

    @property
    def reply_message(self) -> Message:
        return Message(self.bot, self.peer_id, self.reply_object_id)

    @property
    def forward(self) -> Forward:
        return {
            "peer_id": self.peer_id,
            "conversation_message_ids": [self.object_id]
        }

    async def answer(self, text: str = None, attachment: str = None, keyboard: Union[str, Keyboard] = None) -> Message:
        response = await self.bot.execute("messages.send", message=text, peer_ids=self.user_id,
                                          random_id=0, attachment=attachment, keyboard=keyboard)
        message_id = response["response"][0]["conversation_message_id"]

        return Message(self.bot, self.peer_id, message_id)

    async def reply(self, text: str = None, attachment: str = None, keyboard: Union[str, Keyboard] = None) -> Message:
        forward = {
            "peer_id": self.peer_id,
            "conversation_message_ids": [self.object_id],
            "is_reply": 1
        }
        forward = json.dumps(forward)

        response = await self.bot.execute("messages.send", message=text, peer_ids=self.peer_id,
                                          random_id=0, attachment=attachment, keyboard=keyboard,
                                          forward=forward)
        message_id = response["response"][0]["conversation_message_id"]

        return Message(self.bot, self.peer_id, message_id)

    async def send_message(self, text: str = None, attachment: str = None, keyboard: Union[str, Keyboard] = None) -> Message:
        response = await self.bot.execute("messages.send", message=text, peer_ids=self.peer_id,
                                          random_id=0, attachment=attachment, keyboard=keyboard)
        message_id = response["response"][0]["conversation_message_id"]

        return Message(self.bot, self.peer_id, message_id)

    async def send_comment(self, text: str = None, attachment: str = None) -> None:
        await self.bot.execute("wall.createComment",
                               owner_id=self.owner_id, post_id=self.post_id, message=text, attachment=attachment)

    async def mark_as_read(self) -> None:
        await self.bot.execute("messages.markAsRead", peer_id=self.peer_id)

    async def set_typing_status(self, typing_status: str = "typing") -> None:
        await self.bot.execute("messages.setActivity", peer_id=self.peer_id, type=typing_status)

    async def kick_user(self, member_id: int) -> None:
        await self.bot.execute("messages.removeChatUser", chat_id=self.chat_id, member_id=member_id)

    async def edit_chat_name(self, title: str) -> None:
        await self.bot.execute("messages.editChat", chat_id=self.chat_id, title=title)


def get_dispatcher_by_event(bot, event: dict, event_params: EventParams, chain_data: Any) -> Dispatcher:
    event_type = event_params["type"]
    text = event_params["text"]
    user_id = event_params["user_id"]
    peer_id = event_params["peer_id"]
    post_id = event_params["post_id"]
    owner_id = event_params["owner_id"]
    object_id = event_params["object_id"]
    reply = event_params["reply"]
    action = event_params["action"]
    payload = event_params["payload"]

    return Dispatcher(event=event, bot=bot, text=text, user_id=user_id, peer_id=peer_id,
                      post_id=post_id, owner_id=owner_id, reply_text=reply.get("text"),
                      reply_peer_id=reply.get("peer_id"), reply_user_id=reply.get("user_id"),
                      reply_object_id=reply.get("object_id"), chain_data=chain_data, object_id=object_id,
                      action_type=action.get("type"), action_text=action.get("text"), event_type=event_type,
                      action_object_id=action.get("object_id"), action_member_id=action.get("member_id"),
                      payload=payload)
