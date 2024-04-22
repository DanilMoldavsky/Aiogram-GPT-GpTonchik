from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import types
from aiogram.types import \
    Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot
from gpt.gpt import Gpt
from config_reader import config
from storage import set_text, mess_edit_set
from states import ChatGpt

router = Router()
gpt = Gpt(proxy='socks5://wpujiJaH:2nJAhLMm@139.28.233.75:64993')


def escape_markdown_v2(text:str) -> str:
    escape_chars = '_[]()~>#+-=|{}.!' # `*
    server_valid = ''.join("\\" + char if char in escape_chars else char for char in text)
    return server_valid.replace('**', '*')


# @router.message(F.text)
# async def cmd_cancel_no_state(message: Message):
#     await message.answer(
#         text='Сейчас подумаю и отвечу',
#         reply_markup=ReplyKeyboardRemove()
#     )
#     ai_response = await gpt.talk_valid_async(prompts=message.text)
#     ai_valid = escape_markdown_v2(ai_response)
#     await message.answer(
#         text=ai_valid,
#         reply_markup=ReplyKeyboardRemove(),
#         # parse_mode='MarkdownV2'
#     )

@router.callback_query(StateFilter(None), F.data == "gpt_dialog")
async def set_state_gpt(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatGpt.waiting_for_text_chat)
    
    await callback.message.answer(text='Просто отправь сообщение с текстом и Ai ассистент ответит тебе!')

@router.callback_query(ChatGpt.waiting_for_text_chat, F.text)
async def start_gpt_dialog(
    callback: types.CallbackQuery, 
    state: FSMContext, 
    message: Message, 
    autocomplete:bool=True
    ):
    await state.update_data(prompt=message.text)
    await state.set_state(ChatGpt.wait_gpt_response)

    # ai_valid = escape_markdown_v2(ai_response)
    msg_edit_id = await callback.message.answer(
        text='Здесь появится ответ',
        # reply_markup=ReplyKeyboardRemove(),
        # parse_mode='MarkdownV2'
    )
    mess_edit_set(id_user=callback.from_user.id, mess_edit_set=msg_edit_id.message_id)
    
    ai_response = await gpt.talk_valid_async(prompts=message.text)
    construct_resp = ""
    async for response in ai_response:
        construct_resp += response
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=msg_edit_id.message_id,
            text=escape_markdown_v2(construct_resp),
        )
    if autocomplete:
        await state.set_state(state=ChatGpt.waiting_for_text_chat)
        await state.set_data({})
    else:
        await state.clear()
        await state.set_data({})
    