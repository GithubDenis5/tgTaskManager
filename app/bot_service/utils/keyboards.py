from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import labels

alltime_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=labels.TASK_LIST)], [KeyboardButton(text=labels.ADD_TASK)]]
)

under_tasks_list_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=labels.EDIT_TASK_STATUS, callback_data="edit_tasks_status")]
    ]
)

confirm_task_adding = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=labels.YES, callback_data="add_task"),
            InlineKeyboardButton(text=labels.NO, callback_data="denie"),
        ],
    ]
)
