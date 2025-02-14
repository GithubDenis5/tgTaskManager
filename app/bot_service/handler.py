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
from utils import keyboards, messages


logger = setup_logger(__name__)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"cmd_start (from_user={message.from_user.id})")

    await message.answer(
        text=messages.START_MESSAGE, reply_markup=keyboards.alltime_reply_keyboard
    )
