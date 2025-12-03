from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers.start import start_router
from core.settings import settings   

BOT_TOKEN = settings.TELEGRAM_KEY

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)

    await bot.set_my_commands([
        BotCommand(command="/start", description="Начать работу")
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())