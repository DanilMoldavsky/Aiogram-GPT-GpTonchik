from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import \
    Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from gpt.gpt import Gpt
from config_reader import config

router = Router()
gpt = Gpt(proxy='socks5://wpujiJaH:2nJAhLMm@139.28.233.75:64993')


def escape_markdown_v2(text:str) -> str:
    escape_chars = '_[]()~>#+-=|{}.!' # `*
    server_valid = ''.join("\\" + char if char in escape_chars else char for char in text)
    return server_valid.replace('**', '*')


@router.message(F.text)
async def cmd_cancel_no_state(message: Message):
    await message.answer(
        text='Сейчас подумаю и отвечу',
        reply_markup=ReplyKeyboardRemove()
    )
    ai_response = await gpt.talk_valid_async(prompts=message.text)
    ai_valid = escape_markdown_v2(ai_response)
    await message.answer(
        text=ai_valid,
        reply_markup=ReplyKeyboardRemove(),
        # parse_mode='MarkdownV2'
    )