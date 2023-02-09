import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Категории").insert("Затраты")

categories = ["кафе"]
spendings = {"кафе": 12}

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Привет\nПомогу тебе с твоими расходами и буду их прослеживать\n"
                        "Мои команды:\n"
                        "Добавить категорию: /add название_категории\n"
                        "Удалить категорию: /del название_категории\n"
                        "Для того что бы добавить затраты напишите цену и категорию. Например:\n"
                        "1500 кафе", reply_markup=keyboard1)

@dp.message_handler(lambda message: message.text.startswith('/add'))
async def add_category(message: types.Message):
    categories.append(str(message.text[5:]).lower())
    answer_message = "Добавлена категория" + str(message.text[4:]).lower()
    await message.answer(answer_message)

@dp.message_handler(commands=["Категории"])
async def categorii(message: types.Message):
    answer_message = "Категории: \n"
    for i in range(len(categories)):
         answer_message += categories[i]+"\n"
    await message.answer(answer_message)

@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_category(message: types.Message):
    category = str(message.text[5:])
    if (category in categories):
        categories.remove(category)
        del spendings[category]
        answer_message = "Удалена категория" + str(message.text[4:])

    else:
        answer_message = "Такой категории нет"
    await message.answer(answer_message)

@dp.message_handler()
async def message_handler(message: types.Message):
    if message.text=="Категории":
        answer_message = "Категории: \n"
        for i in range(len(categories)):
            answer_message += categories[i]+"\n"
        await message.answer(answer_message)
        return
    if message.text=="Затраты":
        answer_message = "Затраты: \n"
        for key in (spendings.keys()):
            answer_message += key+ " " + str(spendings[key]) +"\n"
        await message.answer(answer_message)
        return

    regexp_result = re.match(r"([\d ]+) (.*)", message.text)
    print(regexp_result)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        await message.answer("Напишите сообщение в формате:\n1500 еда")
        return
    amount = regexp_result.group(1).replace(" ", "")
    category = regexp_result.group(2).strip().lower()
    
    if(category not in categories):
        categories.append(category)
    if(category not in spendings):
        spendings[category] = 0
    spendings[category] += int(amount)
    await message.answer("Затраты добавлены")
    

executor.start_polling(dp)