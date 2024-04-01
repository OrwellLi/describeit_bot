import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from db import Database

import asyncio
from aiogram.dispatcher.filters import Text

TOKEN = "7079774373:AAGDPYQf-ysYfC6MmmQSYmBtztBiHtjfRR0"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database("database.db")




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Registration", callback_data = "login"))
    await bot.send_message(message.chat.id, "In order to use the bot, you need to register", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "login")
async def login(callback_query: types.CallbackQuery):
    if (not db.user_exists(callback_query.from_user.id)):
        db.add_user(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, "Set you're nickname.")

    else:
        await bot.send_message(callback_query.from_user.id, "You're already registred!")
        await bot.send_sticker(callback_query.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Enter your key-phrases", callback_data = "/keyphrases"))
        markup.add(types.InlineKeyboardButton("Check my balance", callback_data = "/balance"))
        await bot.send_message(callback_query.from_user.id, "What would you like to do?", reply_markup=markup)

@dp.message_handler()
async def nicknaming(message: types.Message):
    if message.chat.type == "private":
        if message.text == "lol":
            pass
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if (len(message.text) > 15):
                    await bot.send_message(message.text, "Too large nickname / u need < 15 symbols")
                elif '@' in message.text or '/' in message.text or '"' in message.text or '~' in message.text:
                    await bot.send_message(message.text, "Incorrect symbols in nickname")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Successful regisration!")
                    await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Enter your key-phrases", callback_data = "/keyphrases"))
                    markup.add(types.InlineKeyboardButton("Check my balance", callback_data = "/balance"))
                    await bot.send_message(message.from_user.id, "What would you like to do?", reply_markup=markup)
            else:
                await bot.send_message(message.from_user.id, "???")

    

# @dp.message_handler(commands=['menu'])
# async def begin(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Enter your key-phrases", callback_data = "/keyphrases"))
#     markup.add(types.InlineKeyboardButton("Check my balance", callback_data = "/balance"))
#     await bot.send_message(message.from_user.id, "What would you like to do?", reply_markup=markup)




@dp.callback_query_handler(lambda logg: logg.data == "/keyphrases" or logg.data == "/balance")
async def keyphrases_balance_def(callback_query: types.CallbackQuery):
    if callback_query.data == "/keyphrases":
        await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0YpmCJ4qTSZ5tAyHLhI3Gxnovz2WGAACOAsAAk7kmUsysUfS2U-M0DQE"))

        upload_message = await bot.send_message(callback_query.from_user.id, text="Generating...")
        await asyncio.sleep(2)
        for i in range(100):
            await upload_message.edit_text(text=f"{i}%")
            await asyncio.sleep(0.01)
            if i == 95:
                await upload_message.delete()
                break
        # message.text == 'generate'             
        words = ['apple', 'banana', 'cherry', 'orange', 'pear']
        random_word = random.choice(words)   
        await bot.send_message(callback_query.from_user.id, random_word, )


    elif callback_query.data == "/balance":
        await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
        balance = db.check_balance(callback_query.from_user.id)
        for row in balance:
            balance = row[0]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Back to menu", callback_data = "menu"))
        await bot.send_message(callback_query.from_user.id, f"You have {balance} coins on your balance", reply_markup=markup)
    
@dp.callback_query_handler(lambda call: call.data == "menu")
async def menu(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Enter your key-phrases", callback_data = "/keyphrases"))
    markup.add(types.InlineKeyboardButton("Check my balance", callback_data = "/balance"))
    await bot.send_message(callback_query.from_user.id, "What would you like to do?", reply_markup=markup)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
