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

TOKEN = "7126423804:AAHt8_p1hz0PTY3_ZfTGBqJCq8ULW6BQXN4"
# api_key = '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'
logging.basicConfig(level=logging.INFO)


db = Database("database.db")

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(TOKEN)

router = Router()
flag = 1



class Card(StatesGroup):
    
    set_card_name = State()
    set_card_description = State()
    set_card_keys = State()
    generate = State()

class Promo(StatesGroup):
    promo = State()




@dp.message(CommandStart())
async def start(message: types.Message):
    global flag
    flag = 1
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text = "Зарегистрироваться", callback_data = "login"))
    await bot.send_message(message.chat.id, f"Для того, <b>чтобы пользоваться ботом</b>, вам нужно <b>зарегистрироваться!</b>",parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
flag = 0

@dp.callback_query(F.data == "login")
async def login(callback_query: types.CallbackQuery):
    global flag
    flag = 1
    if (not db.user_exists(callback_query.from_user.id)):
        db.add_user(callback_query.from_user.id)
        db.add_users_balance(callback_query.from_user.id)
        db.add_users_product(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, f"<b>Придуймайте никнейм.</b>", parse_mode=ParseMode.HTML)

    else:
        await bot.send_message(callback_query.from_user.id, "<b>Вы уже зарегистрированы!</b>")
        await bot.send_sticker(callback_query.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "Добавить карточку", callback_data = "/keyphrases"))
        markup.add(types.InlineKeyboardButton(text = "Проверить баланс", callback_data = "/balance"))
        await bot.send_message(callback_query.from_user.id, "⚪ Выберите действие:", reply_markup=markup.as_markup())
        db.set_key( callback_query.from_user.id, "notkey")
flag = 0


@dp.message(Card.set_card_name)
async def process_name(message:types.Message, state: FSMContext):   
    # db.get_product_name(message.from_user.id)
    # db.set_product_name(message.from_user.id, message.text)
    await state.set_state(Card.set_card_description)
    await message.answer("Введите описание товара:")
    # async with state.proxy() as data:
    #     data['card_name'] = message.text
    await state.update_data(card_name = message.text)
    
@dp.message(Card.set_card_description)
async def process_age(message: types.Message, state: FSMContext):
    # db.get_product_descrip(message.from_user.id)
    # db.set_product_descrip(message.from_user.id, message.text)
    await state.set_state(Card.set_card_keys)
    await message.answer("Введите ключевые слова для карточки:")
    # async with state.proxy() as data:
    #     data['card_description'] = message.text
    await state.update_data(card_descrip = message.text)
flag = 0
@dp.message(Card.set_card_keys)
async def process_gender(message: types.Message, state: FSMContext):
    global flag
    flag = 1
    # db.get_product_key(message.from_user.id)
    # db.set_product_key(message.from_user.id, message.text)
    # async with state.proxy() as data:
    #     data['card_keys'] = message.text
    await state.update_data(card_keys = message.text)
    data = await state.get_data()
    card_name = data['card_name']
    card_descrip = data['card_descrip']
    card_keys = data['card_keys']
    markup = InlineKeyboardBuilder()
    await state.set_state(Card.generate)
    markup.add(types.InlineKeyboardButton(text = "Сгенерировать?", callback_data = "/generate"))
    markup.add(types.InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu"))
    await bot.send_message(message.from_user.id, text = f"✉ <b>Ваша карточка для генерации:</b>\n\n<b>Название карточки</b>: {card_name}\n\n<b>Описание  товара</b>: {card_descrip}\n\n<b>Ключевы слова товара</b>: {card_keys}\n\n",parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
    flag = 0
    

@dp.message(Promo.promo)
async def state_promocode(message: types.Message, state: FSMContext):
    await state.update_data(promo = message.text)
    data1 = await state.get_data()
    promo = data1['promo']
    if promo == db.get_promo(1):
        db.plus_balance(message.from_user.id, 5)
        
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu"))
        await bot.send_message(message.from_user.id, text= "🍀 Вы правильно ввели промокод!\n\nК вашему балансу прибавлено <b>5 генераций.</b>", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
        await state.clear()
    else:
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "Вернуться ", callback_data = "menu"))
        await message.answer(f"❌ Вы ввели неправильный промокод!\n\nПопробуйте ввести промокод ещё раз или нажмите кнопку, чтобы вернуться в меню.", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
                

    
    
@dp.callback_query(F.data == "/generate", Card.generate)
async def keyphrases_balance_def(callback_query: types.CallbackQuery, state: FSMContext):
    global flag
    flag = 1
    
    db.minus_balance(callback_query.from_user.id, 1)
    await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0YpmCJ4qTSZ5tAyHLhI3Gxnovz2WGAACOAsAAk7kmUsysUfS2U-M0DQE"))
    upload_message = await bot.send_message(callback_query.from_user.id, text= f"<b>Генерируем...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)
    for i in range(100):
        await upload_message.edit_text(text=f"<b>{i}%</b>", parse_mode=ParseMode.HTML)
        await asyncio.sleep(0.01)
        if i == 94:
            await upload_message.delete()
            break
    data = await state.get_data()
    card_name = data['card_name']
    card_descrip = data['card_descrip']
    card_keys = data['card_keys']
    
    description = generate_product_description(api_key, card_name, card_descrip, card_keys)
    markup1 = InlineKeyboardBuilder()
    markup1.add(types.InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu"))
    await bot.send_message(callback_query.from_user.id, f"<b>Сгенерированное описание для вашей карточки:</b>\n\n<code>{description}</code>",parse_mode=ParseMode.HTML, reply_markup=markup1.as_markup())
    db.set_key(callback_query.from_user.id, "notkey")
    
    # db.set_product_descrip(callback_query.from_user.id, card_descrip)
    db.set_product_key(callback_query.from_user.id, description)
    await callback_query.answer()
 
    await state.clear()

flag = 0



@dp.message()
async def nicknaming(message: Message, state: FSMContext):
    if message.chat.type == "private":
 
        if db.get_signup(message.from_user.id) == "setnickname":
            if (len(message.text) > 15):
                await bot.send_message(message.text, "❌ Too large nickname / u need < 15 symbols")
            elif '@' in message.text or '/' in message.text or '"' in message.text or '~' in message.text:
                await bot.send_message(message.text, "❌ Неправильные символы при вводе никнейма")
            else:
                db.set_nickname(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, "🌀 Успешная регистрация!")
                await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL0YxmCKM8rgXl2qdkHb5n5alqcqOypgAC-woAAm80oUssauxdTRu1eDQE")
                markup = InlineKeyboardBuilder()
                markup.add(types.InlineKeyboardButton(text = "Добавить карточку", callback_data = "/keyphrases"))
                markup.add(types.InlineKeyboardButton(text = "Проверить баланс", callback_data = "/balance"))
                await bot.send_message(message.from_user.id, "Что бы вы хотели сделать?", reply_markup=markup.as_markup())
                db.set_key( message.from_user.id, "notkey")
            # await bot.send_message(message.from_user.id, "What??")
        elif db.get_key(message.from_user.id) == 'key':
            if message.text == "addcard":
                # await state.set_state(Card.set_card_name)
                # await bot.send_message(message.from_user.id, f"📌 <u>The example of the card:</u>\n\n<b>Card NAME:</b>\n\n<b>Card DESCRIPTION:</b>\n\n<b>Card KEY-WORDS:</b>\n\nFor adding a new card description, send the <b>CARD NAME</b>:\n\n",parse_mode = ParseMode.HTML)
                # # await bot.send_message(message.from_user.id, "For adding a new card description, send <addcard>.\n\nThe example of the card:\n\nCards` name\nCards` description")
                # db.set_key(message.from_user.id, "notkey")
                # await message.answer(message.from_user.id, f"Please enter your CARD DESCRIPTION:")
                await state.set_state(Card.set_card_name)
                
                await bot.send_message(message.from_user.id, f"📌 <u>Пример заполнения карточки товара:</u>\n\n<b>Название товара:</b>\n\n<b>Описание товара:</b>\n\n<b>Ключевые слова товара:</b>\n\nДля добавления карточки товара введите <b>название товара</b>:\n\n",parse_mode = ParseMode.HTML)
                # await bot.send_message(message.from_user.id, "For adding a new card description, send <addcard>.\n\nThe example of the card:\n\nCards` name\nCards` description")
                db.set_key(message.from_user.id, "notkey")
            elif message.text != "addcard":
                await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL2CRmDsUfOrCE44ssXVrF9aYpasoQEwACvAsAAv0XmUtFBR2JSwp5RzQE")
                markup = InlineKeyboardBuilder()
                markup.row(types.InlineKeyboardButton(text = "Закрыть", callback_data = "menu"))
                await message.answer(f"❌ Вы ввели неправильные символы...\n\nВведите правильную проверочную фразу или нажмите кнопку <b>ЗАКРЫТЬ</b> для <b>возврата в главное меню</b>", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
            
        elif flag == 0:
            if message.text != "":
                await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL2CRmDsUfOrCE44ssXVrF9aYpasoQEwACvAsAAv0XmUtFBR2JSwp5RzQE")
                markup = InlineKeyboardBuilder()
                markup.add(types.InlineKeyboardButton(text = "Вернуться ", callback_data = "menu"))
                await message.answer(f"❌ Перейдите в меню, чтобы <b>продолжить работу</b> с ботом.", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
                # markup = types.InlineKeyboardMarkup()
                # markup.add(types.InlineKeyboardButton("Generate?", callback_data = "/generate"))
                # markup.add(types.InlineKeyboardButton("Back to menu", callback_data = "menu"))
                # await bot.send_message(message.from_user.id, f"Your key-prase for generating is '{message.text}'\n\n", reply_markup=markup) 


# @dp.message()
# async def entereing(message: Message):
#     if message.chat.type == "private":
#         if message.text != "":
#             await bot.send_sticker(message.from_user.id,"CAACAgIAAxkBAAEL2CRmDsUfOrCE44ssXVrF9aYpasoQEwACvAsAAv0XmUtFBR2JSwp5RzQE")
#             markup = InlineKeyboardBuilder()
#             markup.add(types.InlineKeyboardButton(text = "Вернуться ", callback_data = "menu"))
#             await message.answer(f"❌ Перейдите в меню, чтобы <b>продолжить работу</b> с ботом.", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())


# @dp.callback_query(F.data == "menu", Card.generate)
# async def menu_def(callback_query: types.CallbackQuery, state: FSMContext):
#     db.set_key( callback_query.from_user.id, 'notkey')
#     markup = InlineKeyboardBuilder()
#     markup.add(types.InlineKeyboardButton("ADD CARD", callback_data = "/keyphrases"))
#     markup.add(types.InlineKeyboardButton("CHECK MY BALANCE", callback_data = "/balance"))
#     await bot.send_message(callback_query.from_user.id, f"⚪ <b>What would you like to do?</b>", parse_mode=ParseMode.HTML, reply_markup=markup.as_markup() )
#     await callback_query.answer()
#     await state.clear()



@dp.callback_query(F.data == "/keyphrases")
async def keyphrases_balance_def(callback_query: types.CallbackQuery):
    global flag
    flag = 1
    if callback_query.data == "/keyphrases":
        db.set_key(callback_query.from_user.id, "notkey")  
        balance = db.check_balance(callback_query.from_user.id)
        for row in balance:
            balance = row[0]
        
        if balance <= 0:
            
            markup1 = InlineKeyboardBuilder()
            markup1.add(types.InlineKeyboardButton(text = "Перейти в магазин", callback_data = "shop"))
            markup1.add(types.InlineKeyboardButton(text = "Перейти в меню", callback_data = "menu"))
            await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
            await bot.send_message(callback_query.from_user.id, f"💶 You have <b>{balance}</b> coins on your balance\n\n Do you want <b>to buy</b> some more coins?",parse_mode=ParseMode.HTML, reply_markup=markup1.as_markup())
            await callback_query.answer()
        elif balance > 0:
            await bot.send_message(callback_query.from_user.id, f"🚨 <b>ПРОВЕРКА</b>: Введите 'addcard', чтобы сгенерировать новую карточку!", parse_mode=ParseMode.HTML)
            db.set_key(callback_query.from_user.id, "key")

            # await bot.send_message(callback_query.from_user.id, "Please enter your cards` NAME")
            # markup = types.InlineKeyboardMarkup()
            # markup.add(types.InlineKeyboardButton("Add", callback_data = "add"))
            # await bot.send_message(callback_query.from_user.id, "For adding a new card description, click on the button <Add>", reply_markup=markup)
        flag = 0
        
@dp.callback_query(F.data == "/balance")
async def keyphrases_balance_def(callback_query: types.CallbackQuery):
    global flag
    flag = 1
    if callback_query.data == "/balance":
        # db.set_key( callback_query.from_user.id, 'notkey')
        await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
        balance = db.check_balance(callback_query.from_user.id)
        for row in balance:
            balance = row[0]
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "Перейти в магазин", callback_data = "/shop"))
        markup.add(types.InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu"))
        await bot.send_message(callback_query.from_user.id, f"💶 У вас <b>{balance}</b> генераций.\n\n Вы хотите <b>купить</b> еще <b>генерации карточек</b>?",parse_mode=ParseMode.HTML, reply_markup=markup.as_markup())
        await callback_query.answer()
        flag = 0

        
@dp.callback_query(F.data == "/shop")
async def shop_def(callback_query: types.CallbackQuery):
    global flag
    flag = 1
    if callback_query.data == "/shop":
        
        markup = InlineKeyboardBuilder()
        markup.add(types.InlineKeyboardButton(text = "5 GENS", callback_data = "/5gens"))
        markup.add(types.InlineKeyboardButton(text = "10 GENS", callback_data = "/10gens"))
        markup.add(types.InlineKeyboardButton(text = "20 GENS", callback_data = "/20gens"))
        markup.row(types.InlineKeyboardButton(text = "Ввести промокод", callback_data = "/promo"))
        markup.row(types.InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu"))
        await bot.send_message(callback_query.from_user.id, f"💶 <b>Выберите опцию</b>, которую хотите приобрести или нажмите <b>Ввести промокод</b>, чтобыв ввести <b>промокод:</b>", parse_mode=ParseMode.HTML,reply_markup=markup.as_markup())
        await callback_query.answer()
        flag = 0
        
@dp.callback_query(F.data == "/5gens")
async def shop_onclick_def(callback_query: types.CallbackQuery):
    if callback_query.data == "/5gens":
        await callback_query.answer(text='process buying 5 generations...', show_alert=True)
        
@dp.callback_query(F.data == "/10gens")
async def shop_onclick_def(callback_query: types.CallbackQuery):
    if callback_query.data == "/10gens":
        await callback_query.answer(text='process buying 10 generations...', show_alert=True)
    
@dp.callback_query(F.data == "/20gens")
async def shop_onclick_def(callback_query: types.CallbackQuery):
    if callback_query.data == "/20gens":
        await callback_query.answer(text='process buying 20 generations...', show_alert=True)
        
@dp.callback_query(F.data == "/promo")
async def promo_onclick(callback_query: types.CallbackQuery, state: FSMContext) :
    if callback_query.data == "/promo":
        await bot.send_sticker(callback_query.from_user.id,("CAACAgIAAxkBAAEL0jxmCW0vKg-JkyyYZjS0VkgLxQtzGAACKwwAAiIwWEvIROJY0qdhFDQE"))
        await state.set_state(Promo.promo)
        await bot.send_message(callback_query.from_user.id, f"Введите свой промокод: ")
        

    
@dp.callback_query(F.data == "menu")
async def menu_def(callback_query: types.CallbackQuery):
    global flag
    flag = 1
    db.set_key( callback_query.from_user.id, 'notkey')
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton(text = "Добавить карточку", callback_data = "/keyphrases"))
    markup.add(types.InlineKeyboardButton(text = "Проверить баланс", callback_data = "/balance"))
    await bot.send_message(callback_query.from_user.id, f"⚪ <b>Выберите действие</b>", parse_mode=ParseMode.HTML,reply_markup=markup.as_markup())
    await callback_query.answer()
    flag = 0



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())