from utils import keyboards
from logger import setup_logger
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaDocument,
    Message,
    ReplyKeyboardRemove,
    TelegramObject,
)
from config import messages, labels

from services import task_service
from utils import formaters

logger = setup_logger(__name__)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"cmd_start (from_user={message.from_user.id})")

    await message.answer(
        text=messages.START_MESSAGE, reply_markup=keyboards.alltime_reply_keyboard
    )


@user.message(F.text == labels.TASK_LIST)
async def show_task_list_message(message: Message, state: FSMContext):
    logger.debug(f"user {message.from_user.id} ask tasks list")

    tasks = await task_service.get_tasks(message.from_user.id)

    text = await formaters.format_tasks_list(tasks)

    await message.answer(text=text, reply_markup=keyboards.under_tasks_list_keyboard)
