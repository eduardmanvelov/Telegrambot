from telebot import types

def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Начать", callback_data="start")
    keyboard.add(button)
    return keyboard