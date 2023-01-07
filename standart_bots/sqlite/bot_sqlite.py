from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.storage import FSMContext

from config import API_TOKEN

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class ProfilestatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))

    return kb


def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await message.answer(f'Welcome, {message.from_user.first_name}! Type /create for make profile!',
                         reply_markup=get_kb())
    await message.delete()


@dp.message_handler(commands=['cancel'], state="*")
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Creating was canseled!', reply_markup=get_kb())
    await state.finish()


@dp.message_handler(commands=['create'])
async def create_command(message: types.Message) -> None:
    await message.reply("Lets create your profile!\nTo begin with, send me your photo!",
                        reply_markup=get_cancel())
    await ProfilestatesGroup.photo.set()


@dp.message_handler(lambda message: not message.photo, state=ProfilestatesGroup.photo)
async def check_photo(message: types.Message) -> None:
    await message.reply("It's not a photo, try again!")


@dp.message_handler(content_types=['photo'], state=ProfilestatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply("Now print your name")
    await ProfilestatesGroup.next()


@dp.message_handler(lambda message: not 2 < len(message.text) < 100, state=ProfilestatesGroup.name)
async def check_name(message: types.Message) -> None:
    await message.reply("It's not a name, try again!")


@dp.message_handler(state=ProfilestatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("Now print your age")
    await ProfilestatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or not 5 < float(message.text) < 110,
                    state=ProfilestatesGroup.age)
async def check_age(message: types.Message) -> None:
    await message.reply("It's not a age, try again!")


@dp.message_handler(state=ProfilestatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply("Now print description")
    await ProfilestatesGroup.next()


@dp.message_handler(state=ProfilestatesGroup.description)
async def load_description(message: types.Message, state: FSMContext) -> None:
    await message.answer("Congratulations! Your profile has been created!")
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data["photo"],
                             caption=f"Name: {data['name']}\nAge: {data['age']}\nDescription: {data['description']}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
