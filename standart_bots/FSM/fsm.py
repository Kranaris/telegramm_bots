from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import API_TOKEN

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)


class ClientstatesGroup(StatesGroup):
    photo = State()
    desc = State()


def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


def get_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Start_work'))
    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text='Hello!',
                         reply_markup=get_keyboard())
    await message.delete()


@dp.message_handler(commands=['cancel'], state="*")
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Canceled', reply_markup=get_keyboard())
    await state.finish()


@dp.message_handler(Text(equals='Start_work'), state=None)
async def start_work(message: types.Message) -> None:
    await ClientstatesGroup.photo.set()
    await message.answer('Please, send photo!',
                         reply_markup=get_cancel())


@dp.message_handler(lambda message: not message.photo, state=ClientstatesGroup.photo)
async def cheack_photo(message: types.Message) -> None:
    return await message.reply("This is not a photo")


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientstatesGroup.photo)
async def cheack_photo_2(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await ClientstatesGroup.next()
    await message.reply('Now write text about photo')


@dp.message_handler(state=ClientstatesGroup.desc)
async def desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['desc'] = message.text

    await message.reply('Your photo has been saved!')

    async with state.proxy() as data:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=data['desc'])

    await state.finish()
    await start_work(message)


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)
