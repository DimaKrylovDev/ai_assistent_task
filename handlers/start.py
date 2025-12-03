import openai
from core.settings import settings
from aiogram import Router, types
from aiogram.filters import Command
 
start_router = Router()

@start_router.message(Command('start'))
async def start_message(message: types.Message):
    await message.answer("Welcome to AI assistent")




