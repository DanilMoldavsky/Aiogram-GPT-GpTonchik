import openai
from aiogram import Bot, types
from aiogram import Dispatcher, executor
import logging

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Установка ключей API
token = ""
openai.api_key = ""

# Создание экземпляров
bot = Bot(token)
dp = Dispatcher(bot)

# Словарь для хранения истории сообщений и ответов
conversation_history = {}

# Настройка сообщений
@dp.message_handler()
async def generate_response(message: types.Message):
    try:
        if message.chat.id not in conversation_history:
            conversation_history[message.chat.id] = []

        conversation_history[message.chat.id].append(message.text)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": message.text},
                {"role": "system", "content": conversation_history[message.chat.id][-2] if len(conversation_history[message.chat.id]) > 1 else ""}
            ]
        )

        conversation_history[message.chat.id].append(response.choices[0].message["content"])

        await message.answer(response.choices[0].message["content"])
    except Exception as e:
        logging.exception("Exception occurred")
        await message.answer("An error occurred while processing your request.")

# Запуск 
if name == 'main':
    executor.start_polling(dp, skip_updates=True)