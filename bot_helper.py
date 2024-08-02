import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F
from aiogram.filters.command import Command

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from config_reader import config

logging.basicConfig(level=logging.INFO)

giga = GigaChat(credentials = config.gigachat_token.get_secret_value(), verify_ssl_certs=False)
content = ""
max_tokens = 750

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()

commands_list = ["start", "help", "code", "study", "solutions", "describe", "product", "defense"]

async def main():
    await dp.start_polling(bot)

@dp.message(F.text, Command(commands_list[0]))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Я ваш приятель по хакатонам.\
                         \nЯ отвечаю на следующие команды: \
                         \n/{commands_list[2]} - Написать код, \
                         \n/{commands_list[3]} - Изучить тему, \
                         \n/{commands_list[4]} - Подсказать варианты решений, \
                         \n/{commands_list[5]} - Описать задачу, \
                         \n/{commands_list[6]} - Сформировать продукт, \
                         \n/{commands_list[7]} - Помощь с подготовкой к защите проекта \
                         \nВсе команды можно посмотреть в /help")

@dp.message(F.text, Command(commands_list[1]))
async def cmd_help(message: types.Message):
    await message.reply(f"\n/{commands_list[0]} - Начало работы,\
                         \n/{commands_list[1]} - Все команды,\
                         \n/{commands_list[2]} - Написать код, \
                         \n/{commands_list[3]} - Изучить тему, \
                         \n/{commands_list[4]} - Подсказать варианты решений, \
                         \n/{commands_list[5]} - Описать задачу, \
                         \n/{commands_list[6]} - Сформировать продукт, \
                         \n/{commands_list[7]} - Помощь с подготовкой к защите проекта")

def connect_with_GChat(request: str, add_prompts: str = ''):
    chat = Chat(
           messages=[Messages(role=MessagesRole.USER,
                              content=request)],
           max_tokens=max_tokens
       )
    result = giga.chat(chat)
    return result.content

@dp.message(F.text, Command(commands_list[2]))
async def cmd_code(message: types.Message):
    message_text = message.text
    message_text = message_text.replace(f"/{commands_list[2]}", '')
    if (message_text is not None) and (message_text != ' ') and (message_text != ''):
        await message.reply("Запрос принят, генерирую ответ")
        await message.reply(connect_with_GChat(message_text))
    else: 
        await message.reply("После команды нужно указать описание для действия")

if __name__ == "__main__":
    asyncio.run(main())
