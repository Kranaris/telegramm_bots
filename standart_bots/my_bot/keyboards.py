from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_start_ikb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Show all prodacts", callback_data="get_all_products")],
        [InlineKeyboardButton("Add new product", callback_data="add_new_product")]
    ])
    return ikb

def get_start_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/products_management")]
    ],resize_keyboard=True)

    return kb
def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))
