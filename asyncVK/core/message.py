import json


class Message:
    def __init__(self, bot, peer_id: int, message_id: int):
        self.bot = bot
        self.peer_id = peer_id
        self.message_id = message_id

    async def edit(self, text: str = None, attachment: str = None, keyboard: str = None) -> None:
        await self.bot.execute("messages.edit", peer_id=self.peer_id, conversation_message_id=self.message_id,
                               message=text, attachment=attachment, keyboard=keyboard, keep_forward_messages=1,
                               keep_snippets=1)

    async def delete(self) -> None:
        await self.bot.execute("messages.delete", peer_id=self.peer_id,
                               cmids=self.message_id, delete_for_all=1)

    async def pin(self) -> None:
        await self.bot.execute("messages.pin", peer_id=self.peer_id, conversation_message_id=self.message_id)
