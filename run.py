import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.admin_handlers import admin_router
from app.handlers import router

from app.database.models import async_main

from app.bot import bot

dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(admin_router)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Exit')