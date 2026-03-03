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
