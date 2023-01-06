from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.callback_data import CallbackData
import hashlib
from  config import API_TOKEN

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
cb = CallbackData("ikb", "action")

user_data = ''

async def on_startup(_):
    print(f'Bot have been started!')

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Button_1", callback_data=cb.new("push_1"))],
        [InlineKeyboardButton(text="Button_2", callback_data=cb.new("push_2"))]
    ])
    return ikb


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:
    await message.answer(text=f"Hello, {message.from_user.first_name}\nВведите число.",
                         reply_markup=get_ikb())
    await message.delete()

@dp.message_handler()
async def text_handler(message: types.Message) -> None:
    global user_data
    user_data = message.text
    await message.reply('Данные сохранены')


@dp.callback_query_handler(cb.filter(action='push_1'))
async def push_1(calback: types.CallbackQuery) -> None:
    await calback.answer("Hello")


@dp.callback_query_handler(cb.filter(action='push_2'))
async def push_2(calback: types.CallbackQuery) -> None:
    await calback.answer("World!")

@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or "Echo"
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    input_content = InputTextMessageContent(f'<b>{text}</b> - {user_data}',
                                            parse_mode='html')


    item = InlineQueryResultArticle(
        input_message_content=input_content,
        id=result_id,
        title='Echo_Bot',
        description='I am Bot'
    )
    await bot.answer_inline_query(inline_query_id=inline_query.id, results=[item],
                                  cache_time=1)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup,
                           skip_updates=True)
