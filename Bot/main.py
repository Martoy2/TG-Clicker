import os
import django
from typing import Union, Dict, Any
from aiogram import *
from aiogram import F
from aiogram.filters.command import Command
from aiogram.filters import Filter
from aiogram.filters import StateFilter, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.web_app_data import WebAppData
from aiogram.filters.state import State, StatesGroup
import logging
import asyncio
import DbTools

logging.basicConfig(filename="BotLog.log", filemode="w", encoding='utf-8', level=logging.INFO)

token = 'YOUR TOKEN'

storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(storage=storage)

db = DbTools.UserData()


async def create_start_kb():
    kb = [[types.InlineKeyboardButton(text="Начать кликать", web_app=WebAppInfo(url="https://tiutour.ru/game/clicker/v1/"))],]#https://t.me/RaspClickTest_bot/ClickerRaspTest
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = await create_start_kb()
    if not db.create_user(user_id=message.from_user.id, user_name=message.from_user.username):
        await message.reply("Привет, нажимай ниже что бы начать кликать.", reply_markup=keyboard)
    else:
        await message.reply("Привет, нажимай ниже что бы начать кликать.", reply_markup=keyboard)


async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())

