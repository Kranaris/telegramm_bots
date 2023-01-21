from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

products_cb = CallbackData('product', 'id', 'action')


def get_start_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Show all products", callback_data="get_all_products")],
        [InlineKeyboardButton("Add new product", callback_data="add_new_product")]
    ])
    return ikb


def get_edit_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Edit product", callback_data=products_cb.new(product_id, 'edit'))],
        [InlineKeyboardButton("Delete product", callback_data=products_cb.new(product_id, 'delete'))],
    ])

    return ikb


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/products_management")]
    ], resize_keyboard=True)

    return kb


def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))
