from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from config import API_TOKEN, ADMIN

import sqlite

from keyboards import *

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await sqlite.db_connect()
    print("Data base connected successfully")
    print("The bot has been started successfully!")


class Product_statesGroup(StatesGroup):
    title = State()
    description = State()


class CustomMiddleware(BaseMiddleware):
    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):
        if message.from_user.id != ADMIN:
            print(message.from_user.id)
            raise CancelHandler()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await message.answer(f'Welcome, {message.from_user.first_name}!',
                         reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(commands=['products_management'])
async def products_management_command(message: types.Message) -> None:
    await message.answer(f'Products_management menu.',
                         reply_markup=get_start_ikb())
    await message.delete()


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return
    await message.reply('Add was canceled!', reply_markup=get_start_kb())

    await state.finish()


@dp.callback_query_handler(text='get_all_products')
async def cb_get_all_products(callback: types.CallbackQuery):
    products = await sqlite.get_all_products_bd()

    if not products:
        await callback.answer("You don't have any products!")
        return await callback.answer()

    await callback.message.answer(products)
    await callback.answer()


@dp.callback_query_handler(text='add_new_product')
async def cb_add_new_product(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Text product's title:",
                                  reply_markup=get_cancel())

    await Product_statesGroup.title.set()


@dp.message_handler(state=Product_statesGroup.title)
async def handle_title(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['title'] = message.text

    await message.reply("Text product's description:")
    await Product_statesGroup.next()


@dp.message_handler(state=Product_statesGroup.description)
async def handle_title(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
    await sqlite.create_newproduct(state)
    await message.reply("The product has been added!",
                        reply_markup=get_start_ikb())

    await state.finish()


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return
    await message.reply('Add was canceled!', reply_markup=get_start_kb())

    await state.finish()


if __name__ == "__main__":
    dp.middleware.setup(CustomMiddleware())
    executor.start_polling(dp,
                           on_startup=on_startup,
                           skip_updates=True)
