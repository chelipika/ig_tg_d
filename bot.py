import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from reely.handlers import router
from database.models import async_main
session = AiohttpSession(timeout=300)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()


async def main():
    await async_main()
    print("BOT start polling.....")
    dp.include_router(router=router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
