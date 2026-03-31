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


async def add_doc(tg_id: int, username: str, document, file_name: str, message):
    data = aiohttp.FormData()
    data.add_field("tg_id", str(tg_id))
    data.add_field("username", username if username else "unknown")

    file = await message.bot.get_file(document.file_id)
    file_obj = await message.bot.download_file(file.file_path)

    data.add_field(
        "file",
        file_obj,
        filename=file_name
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(config.url + 'add_document/', data=data) as resp:
            result = await resp.json()

    return result


async def add_doc_by_url(tg_id: int, username: str, url: str):
    data = aiohttp.FormData()
    data.add_field("tg_id", str(tg_id))
    data.add_field("username", username if username else "unknown")
    data.add_field("file_url", url)

    async with aiohttp.ClientSession() as session:
        async with session.post(config.url + 'add_document_by_url/', data=data) as resp:
            result = await resp.json()

    return result
