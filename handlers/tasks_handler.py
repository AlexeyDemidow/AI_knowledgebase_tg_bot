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


async def ask_backend(tg_id, username, message):
    payload = {
        "tg_id": str(tg_id),
        "username": username,
        "message": message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(config.url + 'chat/', json=payload) as resp:
            return await resp.json()