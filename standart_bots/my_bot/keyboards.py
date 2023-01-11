from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

def get_profile_data():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/get_profile_data'))