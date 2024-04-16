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


@router.message(F.text)
async def cmd_cancel_no_state(message: Message):
    await message.answer(
        text='Сейчас подумаю и отвечу',
        reply_markup=ReplyKeyboardRemove()
    )
    ai_response = gpt.talk_valid_markdown(prompts=message.text)
    await message.answer(
        text=ai_response,
        reply_markup=ReplyKeyboardRemove()
    )