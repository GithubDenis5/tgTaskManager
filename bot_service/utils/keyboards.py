from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_service.config import labels
from bot_service.services import task_service
from bot_service.config.keyboards import KEYBOARD_PAGE_SIZE
from math import ceil

from bot_service.logger import setup_logger

logger = setup_logger(__name__)

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


async def tasks_list_keyboard(cur_page: int, tg_id: int):

    tasks_list = await task_service.get_tasks(tg_id)

    logger.debug(tasks_list)

    if not tasks_list:
        return None

    pages_num = ceil(len(tasks_list) / KEYBOARD_PAGE_SIZE)
    from_i = KEYBOARD_PAGE_SIZE * (cur_page - 1)
    to_i = min(len(tasks_list), KEYBOARD_PAGE_SIZE * cur_page)
    keyboard = InlineKeyboardBuilder()

    for i in range(from_i, to_i):
        keyboard.row(
            InlineKeyboardButton(
                text=tasks_list[i]["name"],
                callback_data=f"task_{tasks_list[i]["task_id"]}_{cur_page}",
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            text=labels.BACK,
            callback_data=(f"page_task_{cur_page-1}" if cur_page - 1 > 0 else "_"),
        ),
        InlineKeyboardButton(text=f"{cur_page}/{pages_num}", callback_data="_"),
        InlineKeyboardButton(
            text=labels.FORWARD,
            callback_data=(f"page_task_{cur_page+1}" if cur_page < pages_num else "_"),
        ),
    )

    keyboard.row(InlineKeyboardButton(text=labels.RETURN, callback_data="show_tasks_list_message"))

    return keyboard.as_markup()
