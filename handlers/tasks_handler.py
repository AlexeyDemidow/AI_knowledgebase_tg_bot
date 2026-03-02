import aiohttp

from bot_settings import config


async def create_user(tg_id: str, username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(config.url + '/user_create/' + f'?username={username}&tg_id={tg_id}') as response:
            return await response.json()
