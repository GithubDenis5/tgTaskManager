from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import labels

alltime_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=labels.TASK_LIST)], [KeyboardButton(text=labels.ADD_TASK)]]
)
