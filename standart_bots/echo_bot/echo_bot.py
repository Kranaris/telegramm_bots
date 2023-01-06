from aiogram import Dispatcher, executor, Bot, types
from standart_bots.first_bot_with_keyboards.config import API_TOKEN
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked
import asyncio

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
cd = CallbackData("ikb", "abc")

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="button", callback_data=cd.new("t1"))]
])

@dp.errors_handler(exception=BotBlocked) #Обработка исключения
async def error(update, exception):
    print("Бота заблокировали")
    return True

@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await asyncio.sleep(2)
    await message.answer(text="echo_bot",
                         reply_markup=ikb)
    await message.delete()

@dp.callback_query_handler(cd.filter())
async def qq(callback: types.CallbackQuery, callback_data: dict) -> None:
    print(callback.data)
    if callback_data["abc"] == "t1":
        await callback.answer("Yooo!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
