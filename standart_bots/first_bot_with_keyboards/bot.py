from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from config import API_TOKEN
from aiogram.dispatcher.filters import Text
from datetime import datetime
from keyboards import kb_main, ikb_begin
from random import randint

help_comand = """
<b>/start</b> - <em>перезапустить бота</em>
<b>/begin</b> - <em>начать работу с ботом</em>
<b>/help</b> - <em>список команд</em>
<b>/description</b> - <em>описание бота</em>
"""

description = """
<b>Описание Бота</b>:
Бот учится всяким штукам, скоро все будет!
"""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print(f'Bot have been started! {datetime.now()}')


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(text=f'Приветствую, {message.from_user.first_name}!',
                         parse_mode="html",
                         reply_markup=kb_main)
    await message.delete()


@dp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(text=help_comand,
                         parse_mode="html")
    await message.delete()


@dp.message_handler(commands="description")
async def description_command(message: types.Message):
    await message.answer(text=description,
                         parse_mode="html")
    await message.delete()


@dp.message_handler(commands="begin")
async def begin_command(message: types.Message):
    x = randint(0, 9)
    y = randint(0, 9)
    res = x + y
    await message.answer(text=f"Выбери вариант ответа\n{x} + {y} = {res}?",
                         parse_mode="html",
                         reply_markup=ikb_begin)
    await message.delete()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('1'))
async def answer(callback: types.CallbackQuery) -> None:
    if callback.data == "1yes":
        await callback.answer(text="Отлично!")
    elif callback.data == "1no":
        await callback.answer(text="Провал!")
    else:
        await callback.message.answer(text="Вы в главном меню.",
                                      reply_markup=kb_main)
        await callback.answer()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
