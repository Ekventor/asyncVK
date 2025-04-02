from typing import Union
import json

from .keyboard import Keyboard


class Message:
    def __init__(self, bot, peer_id: int, message_id: int):
        self.bot = bot
        self.peer_id = peer_id
        self.message_id = message_id

    async def edit(self, text: str = None, attachment: str = None, keyboard: Union[str, Keyboard] = None) -> None:
        await self.bot.execute("messages.edit", peer_id=self.peer_id, conversation_message_id=self.message_id,
                               message=text, attachment=attachment, keyboard=keyboard, keep_forward_messages=1,
                               keep_snippets=1)

    async def delete(self) -> None:
        await self.bot.execute("messages.delete", peer_id=self.peer_id,
                               cmids=self.message_id, delete_for_all=1)

    async def pin(self) -> None:
        await self.bot.execute("messages.pin", peer_id=self.peer_id, conversation_message_id=self.message_id)


class MessageTemplate:
    def __init__(self, bot, text: str = None, attachment: str = None,
                 keyboard: Union[str, Keyboard] = None, forward: dict = None):
        self.bot = bot
        self.text = text
        self.attachment = attachment
        self.keyboard = keyboard

        self.forward = None
        if forward is not None:
            self.forward = json.dumps(forward)

    async def send_to(self, peer_id: Union[str, int]) -> Union[list[Message], Message]:
        response = await self.bot.execute("messages.send", message=self.text, peer_ids=peer_id,
                                          random_id=0, attachment=self.attachment, keyboard=self.keyboard,
                                          forward=self.forward)

        messages = []
        for message in response["response"]:
            messages.append(Message(self.bot, message["peer_id"], message["conversation_message_id"]))

        if len(messages) == 1:
            return messages[0]
        return messages
