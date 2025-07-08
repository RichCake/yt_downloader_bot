import asyncio
import logging
import os.path
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram import F

from dotenv import load_dotenv

import downloader
import utils

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
YOUTUBE_REGEX = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(F.text.regexp(YOUTUBE_REGEX))
async def download_handler(message: Message) -> None:
    try:
        await message.answer("Скачиваем видео...")
        path = await asyncio.to_thread(downloader.download, message.text)
        if os.path.isfile(path):
            video = FSInputFile(path)
            w, h = utils.get_video_resolution(path)
            await message.answer_video(video, width=w, height=h)
        else:
            print("ОШИБКА: Видео не скачано или не найдено")
            await message.answer("Не удалось скачать видео :(")
    except Exception as e:
        print(e)
        await message.answer("Error!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())