from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton('generate')
btnsubs = KeyboardButton('subs')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnsubs)