import openai
import sys
import logging
import random
from aiogram import Bot, Dispatcher, types
from db import Database


import asyncio
# from aiogram.filters import Text
from aiogram import F, Router

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import aiogram.utils.markdown as md
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from product_description_generator import generate_product_description
from aiogram.types import Message
logging.basicConfig(level=logging.INFO)

TOKEN = "7079774373:AAGDPYQf-ysYfC6MmmQSYmBtztBiHtjfRR0"

logging.basicConfig(level=logging.INFO)


db = Database("database.db")

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(TOKEN)

router = Router()



class Card(StatesGroup):
    
    set_card_name = State()
    set_card_description = State()
    set_card_keys = State()
    generate = State()




@dp.message(CommandStart())
async def start(message: types.Message):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text = "Registration", callback_data = "login"))
    await bot.send_message(message.chat.id, "In order to use the bot, you need to register", reply_markup=markup.as_markup())


@dp.callback_query(F.data == "login")
async def login(callback_query: types.CallbackQuery):
    if (not db.user_exists(callback_query.from_user.id)):
        db.add_user(callback_query.from_user.id)
        db.add_users_balance(callback_query.from_user.id)
        db.add_users_product(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, "Set you're nickname.")

    else:
        await bot.send_message(callback_query.from_user.id, "You're already registred!")
        await bot.send_sticker(callback_query.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "ADD CARD", callback_data = "/keyphrases"))
        markup.add(types.InlineKeyboardButton(text = "CHECK MY BALANCE", callback_data = "/balance"))
        await bot.send_message(callback_query.from_user.id, "⚪ What would you like to do?", reply_markup=markup.as_markup())
        db.set_key( callback_query.from_user.id, "notkey")

@dp.message()
async def nicknaming(message: Message, state: FSMContext):
    if message.chat.type == "private":
 
        if db.get_signup(message.from_user.id) == "setnickname":
            if (len(message.text) > 15):
                await bot.send_message(message.text, "❌ Too large nickname / u need < 15 symbols")
            elif '@' in message.text or '/' in message.text or '"' in message.text or '~' in message.text:
                await bot.send_message(message.text, "❌ Incorrect symbols in nickname")
            else:
                db.set_nickname(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, "🌀 Successful regisration!")
                await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
                markup = InlineKeyboardBuilder()
                markup.add(types.InlineKeyboardButton(text = "ADD CARD", callback_data = "/keyphrases"))
                markup.add(types.InlineKeyboardButton(text = "CHECK MY BALANCE", callback_data = "/balance"))
                await bot.send_message(message.from_user.id, "What would you like to do?", reply_markup=markup.as_markup())
                db.set_key( message.from_user.id, "notkey")
            await bot.send_message(message.from_user.id, "What??")
        elif db.get_key(message.from_user.id) == 'key':
            if message.text == "addcard":
                # await state.set_state(Card.set_card_name)
                # await bot.send_message(message.from_user.id, f"📌 <u>The example of the card:</u>\n\n<b>Card NAME:</b>\n\n<b>Card DESCRIPTION:</b>\n\n<b>Card KEY-WORDS:</b>\n\nFor adding a new card description, send the <b>CARD NAME</b>:\n\n",parse_mode = ParseMode.HTML)
                # # await bot.send_message(message.from_user.id, "For adding a new card description, send <addcard>.\n\nThe example of the card:\n\nCards` name\nCards` description")
                # db.set_key(message.from_user.id, "notkey")
                # await message.answer(message.from_user.id, f"Please enter your CARD DESCRIPTION:")
                await state.set_state(Card.set_card_name)
                
                await bot.send_message(message.from_user.id, f"📌 <u>The example of the card:</u>\n\n<b>Card NAME:</b>\n\n<b>Card DESCRIPTION:</b>\n\n<b>Card KEY-WORDS:</b>\n\nFor adding a new card description, send the <b>CARD NAME</b>:\n\n",parse_mode = ParseMode.HTML)
                # await bot.send_message(message.from_user.id, "For adding a new card description, send <addcard>.\n\nThe example of the card:\n\nCards` name\nCards` description")
                db.set_key(message.from_user.id, "notkey")
            elif message.text != "addcard":
                await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL2CRmDsUfOrCE44ssXVrF9aYpasoQEwACvAsAAv0XmUtFBR2JSwp5RzQE")
                markup = InlineKeyboardBuilder()
                markup.row(types.InlineKeyboardButton(text = "CANCEL", callback_data = "menu"))
                await message.answer(f"❌ You entered the wrong symbols...\n\nSend the right symbols, or click <b>CANCEL</b> button to <b>return to menu</b>", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
                
                # markup = types.InlineKeyboardMarkup()
                # markup.add(types.InlineKeyboardButton("Generate?", callback_data = "/generate"))
                # markup.add(types.InlineKeyboardButton("Back to menu", callback_data = "menu"))
                # await bot.send_message(message.from_user.id, f"Your key-prase for generating is '{message.text}'\n\n", reply_markup=markup)


@dp.message(Card.set_card_name)
async def process_name(message:types.Message, state: FSMContext):
    # db.get_product_name(message.from_user.id)
    # db.set_product_name(message.from_user.id, message.text)
    await state.set_state(Card.set_card_description)
    await message.answer("Please enter your CARD DESCRIPTION:")
    # async with state.proxy() as data:
    #     data['card_name'] = message.text
    await state.update_data(card_name = message.text)
    
    

@dp.message(Card.set_card_description)
async def process_age(message: types.Message, state: FSMContext):
    # db.get_product_descrip(message.from_user.id)
    # db.set_product_descrip(message.from_user.id, message.text)
    await state.set_state(Card.set_card_keys)
    await message.answer("Please enter your CARD KEY-WORDS:")
    # async with state.proxy() as data:
    #     data['card_description'] = message.text
    await state.update_data(card_descrip = message.text)
    


@dp.message(Card.set_card_keys)
async def process_gender(message: types.Message, state: FSMContext):
    # db.get_product_key(message.from_user.id)
    # db.set_product_key(message.from_user.id, message.text)
    # async with state.proxy() as data:
    #     data['card_keys'] = message.text
    await state.update_data(card_keys = message.text)
    data = await state.get_data()
    card_name = data['card_name']
    card_descrip = data['card_description']
    card_keys = data['card_keys']
    markup = InlineKeyboardBuilder()
    await state.set_state(Card.generate)
    markup.add(types.InlineKeyboardButton(text = "GENERATE?", callback_data = "/generate"))
    markup.add(types.InlineKeyboardButton(text = "BACK TO MENU", callback_data = "menu"))
    await bot.send_message(message.from_user.id, text = f"✉ <b>Your card for generating is:</b>\n\n<b>Card NAME</b>: {card_name}\n\n<b>Card DESCRIPTION</b>: {card_descrip}\n\n<b>Card KEY-WORDS</b>: {card_keys}\n\n",parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
    

@dp.callback_query(F.data == "/generate", Card.generate)
async def keyphrases_balance_def(callback_query: types.CallbackQuery, state: FSMContext):
    
    db.minus_balance(callback_query.from_user.id, 1)
    await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0YpmCJ4qTSZ5tAyHLhI3Gxnovz2WGAACOAsAAk7kmUsysUfS2U-M0DQE"))
    upload_message = await bot.send_message(callback_query.from_user.id, text= "Generating...", )
    await asyncio.sleep(2)
    for i in range(100):
        await upload_message.edit_text(text=f"{i}%")
        await asyncio.sleep(0.01)
        if i == 94:
            await upload_message.delete()
            break
    data = await state.get_data()
    card_name = data['card_name']
    card_descrip = data['card_description']
    card_keys = data['card_keys']
    
    # description = generate_product_description(api_key, card_name, card_descrip, card_keys)
    markup1 = InlineKeyboardBuilder()
    markup1.add(types.InlineKeyboardButton(text = "BACK TO MENU", callback_data = "menu"))
    await bot.send_message(callback_query.from_user.id, f"<b>Generated full-description for your card:</b>\n\n{card_name}",parse_mode=ParseMode.HTML, reply_markup=markup1.as_markup())
    db.set_key(callback_query.from_user.id, "notkey")
    
    # db.set_product_descrip(callback_query.from_user.id, card_descrip)
    db.set_product_keys(callback_query.from_user.id, card_keys)
    await callback_query.answer()
    await state.clear()


@dp.callback_query(F.data == "menu", Card.generate)
async def menu_def(callback_query: types.CallbackQuery, state: FSMContext):
    db.set_key( callback_query.from_user.id, 'notkey')
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton("ADD CARD", callback_data = "/keyphrases"))
    markup.add(types.InlineKeyboardButton("CHECK MY BALANCE", callback_data = "/balance"))
    await bot.send_message(callback_query.from_user.id, f"⚪ <b>What would you like to do?</b>", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup() )
    await callback_query.answer()
    await state.clear()


@dp.callback_query(F.data == "/keyphrases")
async def keyphrases_balance_def(callback_query: types.CallbackQuery):

    if callback_query.data == "/keyphrases":
        db.set_key(callback_query.from_user.id, "notkey")  
        balance = db.check_balance(callback_query.from_user.id)
        for row in balance:
            balance = row[0]
        
        if balance <= 0:
            
            markup1 = InlineKeyboardBuilder()
            markup1.add(types.InlineKeyboardButton(text = "SHOP", callback_data = "shop"))
            markup1.add(types.InlineKeyboardButton(text = "BACK TO MENU", callback_data = "menu"))
            await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
            await bot.send_message(callback_query.from_user.id, f"💶 You have <b>{balance}</b> coins on your balance\n\n Do you want <b>to buy</b> some more coins?",parse_mode=ParseMode.HTML, reply_markup=markup1.as_markup())
            await callback_query.answer()
        elif balance > 0:
            await bot.send_message(callback_query.from_user.id, f"🚨 <b>CHECK</b>: Enter 'addcard' to generate a new card!", parse_mode=ParseMode.HTML)
            db.set_key(callback_query.from_user.id, "key")

            # await bot.send_message(callback_query.from_user.id, "Please enter your cards` NAME")
            # markup = types.InlineKeyboardMarkup()
            # markup.add(types.InlineKeyboardButton("Add", callback_data = "add"))
            # await bot.send_message(callback_query.from_user.id, "For adding a new card description, click on the button <Add>", reply_markup=markup)
            
        
@dp.callback_query(F.data == "/balance")
async def keyphrases_balance_def(callback_query: types.CallbackQuery):
    if callback_query.data == "/balance":
        db.set_key( callback_query.from_user.id, 'notkey')
        await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
        balance = db.check_balance(callback_query.from_user.id)
        for row in balance:
            balance = row[0]
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "Go to shop", callback_data = "shop"))
        markup.add(types.InlineKeyboardButton(text = "Back to menu", callback_data = "menu"))
        await bot.send_message(callback_query.from_user.id, f"💶 You have <b>{balance}</b> coins on your balance.\n\n Do you want <b>to buy</b> some more <b>coins</b>?",parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
        await callback_query.answer()
        

    
@dp.callback_query(F.data == "menu")
async def menu_def(callback_query: types.CallbackQuery):
    db.set_key( callback_query.from_user.id, 'notkey')
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton(text = "Add new card", callback_data = "/keyphrases"))
    markup.add(types.InlineKeyboardButton(text = "Check my balance", callback_data = "/balance"))
    await bot.send_message(callback_query.from_user.id, f"⚪ <b>What would you like to do?</b>", parse_mode=ParseMode.HTML,reply_markup=markup.as_markup())
    await callback_query.answer()



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())