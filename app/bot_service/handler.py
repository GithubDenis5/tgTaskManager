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
from config import messages, labels, states

from services import task_service
from utils import formaters

logger = setup_logger(__name__)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"cmd_start (from_user={message.from_user.id})")
    await state.clear()

    await message.answer(
        text=messages.START_MESSAGE, reply_markup=keyboards.alltime_reply_keyboard
    )


@user.message(F.text == labels.TASK_LIST)
async def show_task_list_message(message: Message, state: FSMContext):
    logger.debug(f"user {message.from_user.id} ask tasks list")
    await state.clear()

    tasks = await task_service.get_tasks(message.from_user.id)

    text = await formaters.format_tasks_list(tasks)

    await message.answer(text=text, reply_markup=keyboards.under_tasks_list_keyboard)


@user.message(F.text == labels.ADD_TASK)
async def task_adding_name(message: Message, state: FSMContext):
    logger.debug(f"user {message.from_user.id} start adding task")

    await state.clear()
    await message.answer(text=messages.ENTER_TASK_NAME)
    await state.set_state(states.AddTask.name)


@user.message(states.AddTask.name)
async def task_adding_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=messages.ENTER_DESCRIPTION)
    await state.set_state(states.AddTask.description)


@user.message(states.AddTask.description)
async def task_adding_deadline_date(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=messages.ENTER_DEADLINE_DATE)
    await state.set_state(states.AddTask.deadline_date)


@user.message(states.AddTask.deadline_date)
async def task_adding_deadline_time(message: Message, state: FSMContext):
    await state.update_data(deadline_date=message.text)
    await message.answer(text=messages.ENTER_DEADLINE_TIME)
    await state.set_state(states.AddTask.deadline_time)


@user.message(states.AddTask.deadline_time)
async def task_adding_notification_date(message: Message, state: FSMContext):
    await state.update_data(deadline_time=message.text)
    await message.answer(text=messages.ENTER_NOTIFICATION_DATE)
    await state.set_state(states.AddTask.notification_date)


@user.message(states.AddTask.notification_date)
async def task_adding_notification_time(message: Message, state: FSMContext):
    await state.update_data(notification_date=message.text)
    await message.answer(text=messages.ENTER_NOTIFICATION_TIME)
    await state.set_state(states.AddTask.notification_time)


@user.message(states.AddTask.notification_time)
async def task_adding_show_fields(message: Message, state: FSMContext):
    await state.update_data(notification_time=message.text)

    data = await state.get_data()
    name = data["name"]
    description = data["description"]
    deadline_date = data["deadline_date"]
    deadline_time = data["deadline_time"]
    notification_date = data["notification_date"]
    notification_time = data["notification_time"]

    task_service.add_task(data)

    text = messages.CONFIRM_TASK_ADDING + messages.TASK_FORMATER.format(
        name, description, deadline_date, deadline_time, notification_date, notification_time
    )

    await message.answer(text=text, reply_markup=keyboards.confirm_task_adding)
