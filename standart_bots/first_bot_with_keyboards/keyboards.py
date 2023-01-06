from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

kb_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_main1 = KeyboardButton(text="/begin")
kb_main2 = KeyboardButton(text="/help")
kb_main3 = KeyboardButton(text="/description")
kb_main.add(kb_main1).insert(kb_main2).add(kb_main3)

ikb_begin = InlineKeyboardMarkup(row_width=2)
ikb_begin1 = InlineKeyboardButton(text="Да", callback_data="1yes")
ikb_begin2 = InlineKeyboardButton(text="Нет", callback_data="1no")
ikb_begin3 = InlineKeyboardButton(text="Главное меню",  callback_data="1main")
ikb_begin.add(ikb_begin1, ikb_begin2).add(ikb_begin3)

