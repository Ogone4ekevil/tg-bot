import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import logging

from app.handlers import router
from database import create_db


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token='7941965797:AAGklGRIj62bYa_iioVKqLYlvstjwrvgUn4',
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)

    create_db()
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
