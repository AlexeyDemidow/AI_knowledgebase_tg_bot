import aiohttp

from bot_settings import config


async def create_user(tg_id: str, username: str):
    async with aiohttp.ClientSession() as session:
        data = {
            'tg_id': tg_id,
            'username': username,
        }
        async with session.post(config.url + 'user_create/', json=data) as response:
            return await response.json()


async def ask_backend(tg_id: int, username: str, message: str, chat_mode: str, doc_id: str):
    payload = {
        "tg_id": str(tg_id),
        "username": username,
        "message": message,
        "chat_mode": chat_mode,
        "doc_id": doc_id,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(config.url + 'chat/', json=payload) as resp:
            return await resp.json()


async def show_docs(tg_id: str, username: str):
    async with aiohttp.ClientSession() as session:
        data = {
            'tg_id': str(tg_id),
            'username': username,
        }

        async with session.get(config.url + 'show_docs/', params=data) as resp:
            return await resp.json()


async def del_doc(tg_id: str, username: str, doc_id: str):
    async with aiohttp.ClientSession() as session:
        data = {
            'tg_id': str(tg_id),
            'username': username,
            'doc_id': doc_id,
        }

        async with session.delete(config.url + 'delete_doc/', params=data) as resp:
            return await resp.json()
