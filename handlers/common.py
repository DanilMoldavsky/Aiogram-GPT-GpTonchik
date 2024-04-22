from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import \
    Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Dict, Any

from kb.gptkb import gpt_keyboard
# from states import DeleteCommon, SaveCommon

router = Router()


@router.message(Command(commands=["start", "gpt"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Привет!\nЕсли вы хотите пообщаться с ChatGpt4, нажмите на кнопку ниже\nСкоро появятся новые функции!",
        reply_markup=gpt_keyboard()
    )

# Нетрудно догадаться, что следующие два хэндлера можно 
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


# @router.message(CommandStart(magic=F.args == "add"))
# @router.message(Command("save"), StateFilter(None))
# async def cmd_save(message: Message, state: FSMContext):
#     await state.set_state(SaveCommon.waiting_for_save_start)
#     await message.answer("Отправь мне сообщение с ссылкой или фото для сохранения.")


# @router.message(Command("save"))
# async def save_start(message: Message, state: FSMContext):
#     await state.set_state(SaveCommon.waiting_for_save_start)
#     await message.answer("Отправь мне сообщение с ссылкой или фото для сохранения.")

# @router.message(Command("delete"), StateFilter(None))
# async def cmd_delete(message: Message, state: FSMContext):
#     kb = []
#     kb.append([
#         InlineKeyboardButton(
#             text="Выбрать ссылку",
#             switch_inline_query_current_chat="links"
#         )
#     ])
#     kb.append([
#         InlineKeyboardButton(
#             text="Выбрать изображение",
#             switch_inline_query_current_chat="images"
#         )
#     ])
#     await state.set_state(DeleteCommon.waiting_for_delete_start)
#     await message.answer(
#         text="Выберите, что хотите удалить:",
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
#     )
    
@router.message(Command(commands=["db"]))
async def cmd_start(message: Message, state: FSMContext, response: dict):
    await state.clear()
    
    await message.answer(
        # text=f"{pgCount} стран в базе данных по usa"
        #      "блюда (/food) или напитки (/drinks).",
        text=f"{response}",
        reply_markup=ReplyKeyboardRemove()
    )
