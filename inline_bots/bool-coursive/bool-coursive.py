import uuid

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from config import API_TOKEN

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print(f'Bot have been started!')


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:
    await message.answer(text=f"Hello, {message.from_user.first_name}!")
    await message.delete()


@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or "Empty"
    input_content_bold = types.InputTextMessageContent(message_text=f'*{text}*',
                                                  parse_mode="markdown")
    input_content_italic = types.InputTextMessageContent(message_text=f'_{text}_',
                                                  parse_mode="markdown")

    item_1 = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        input_message_content=input_content_bold,
        title='Bold',
        description=text,
        thumb_url='https://www.boldwebdesign.com.au/colour-palettes/wp-content/uploads/2019/07/bold-logo.jpg'
    )

    item_2 = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        input_message_content=input_content_italic,
        title='Italic',
        description=text,
        thumb_url='https://mms.businesswire.com/media/20181115005242/en/690818/23/Italic_Logo.jpg'
    )

    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item_1, item_2],
                                  cache_time=1)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup,
                           skip_updates=True)
