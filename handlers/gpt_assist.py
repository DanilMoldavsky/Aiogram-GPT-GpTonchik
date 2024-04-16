from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import \
    Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from gpt.gpt import Gpt
import conf

router = Router()
gpt = Gpt(proxy=conf.ADDRESS_PROXY)


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
    ai_response = gpt.talk_valid_markdown(prompts=message.text)
    ai_valid = escape_markdown_v2(ai_response)
    await message.answer(
        text=ai_valid,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='MarkdownV2'
    )