from typing import Any
import aiohttp


class Dispatcher:
    def __init__(self, event: dict, token: str, text: str = None, user_id: int = None, peer_id: int = None,
                 post_id: int = None, owner_id: int = None, chain_data: Any = None):
        self.token = token
        self.user_id = user_id
        self.peer_id = peer_id
        self.post_id = post_id
        self.owner_id = owner_id
        self.event = event
        self.text = text
        self.chain_data = chain_data

    async def answer(self, text: str, attachment: str = None, keyboard: str = None) -> None:
        params = f"user_id={self.user_id}&message={text}&random_id=0"
        if attachment is not None:
            params += f"&attachment={attachment}"
        if keyboard is not None:
            params += f"keyboard={keyboard}"
        params += f"&access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            await session.post("https://api.vk.com/method/messages.send", params=params)

    async def send_message(self, text: str, attachment: str = None, keyboard: str = None) -> None:
        params = f"peer_id={self.peer_id}&message={text}&random_id=0"
        if attachment is not None:
            params += f"&attachment={attachment}"
        if keyboard is not None:
            params += f"&keyboard={keyboard}"
        params += f"&access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            await session.post("https://api.vk.com/method/messages.send", params=params)

    async def send_comment(self, text: str, attachment: str = None) -> None:
        params = f"owner_id={self.owner_id}&post_id={self.post_id}&message={text}"
        if attachment is not None:
            params += f"&attachment={attachment}"
        params += f"&access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            await session.post("https://api.vk.com/method/wall.createComment", params=params)

    async def mark_as_read(self) -> None:
        params = f"peer_id={self.peer_id}&access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            await session.post("https://api.vk.com/method/messages.markAsRead", params=params)

    async def set_typing_status(self, typing_status: str = "typing") -> None:
        params = f"peer_id={self.peer_id}&type={typing_status}&access_token={self.token}&v=5.126"

        async with aiohttp.ClientSession() as session:
            await session.post("https://api.vk.com/method/messages.setActivity", params=params)


def get_dispatcher_by_event(token: str, event: dict, event_params: dict, chain_data: Any) -> Dispatcher:
    text = event_params["text"]
    user_id = event_params["user_id"]
    peer_id = event_params["peer_id"]
    post_id = event_params["post_id"]
    owner_id = event_params["owner_id"]

    return Dispatcher(event=event, token=token, text=text, user_id=user_id, peer_id=peer_id,
                      post_id=post_id, owner_id=owner_id, chain_data=chain_data)
