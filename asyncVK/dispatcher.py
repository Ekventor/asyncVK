import aiohttp


class Dispatcher:
    def __init__(self, event: dict, token: str, text: str, user_id: int, peer_id: int = None, post_id: int = None, owner_id: int = None):
        self.token = token
        self.user_id = user_id
        self.peer_id = peer_id
        self.post_id = post_id
        self.owner_id = owner_id
        self.event = event
        self.text = text

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
