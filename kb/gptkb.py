from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



# @router.message(SaveCommon.waiting_for_save_start, F.photo[-1].as_("photo"))
# async def save_image(message: Message, photo: PhotoSize, state: FSMContext):
#     add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)
    
#     kb = [[InlineKeyboardButton(
#         text="Попробовать",
#         switch_inline_query="images"
#     )]]
#     await message.answer(
#         text="Изображение сохранено!",
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
#         )
#     await state.clear()
    


def gpt_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Разговор с ChatGpt4", 
        callback_data="gpt_dialog",
        )
	)
    return builder.as_markup()