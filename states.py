from aiogram.fsm.state import StatesGroup, State

class ChatGpt(StatesGroup):
    waiting_for_text_chat = State()
    wait_gpt_response = State()

# class DeleteCommon(StatesGroup):
#     waiting_for_delete_start = State()

# class TextSave(StatesGroup):
#     waiting_for_title = State()
#     waiting_for_description = State()