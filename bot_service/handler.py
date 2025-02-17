from bot_service.utils import keyboards
from bot_service.logger import setup_logger
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
from bot_service.config import messages, labels, states

from bot_service.services import task_service
from bot_service.utils import formaters

logger = setup_logger(__name__)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"cmd_start (from_user={message.from_user.id})")
    await state.clear()

    await message.answer(
        text=messages.START_MESSAGE, reply_markup=keyboards.alltime_reply_keyboard
    )


@user.callback_query(F.data == "denie")
async def denie_action(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(text=messages.ACTION_DENIED)

    await state.clear()


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

    try:
        await state.update_data(deadline=formaters.convert_datetime(deadline_date, deadline_time))
        await state.update_data(
            notification=formaters.convert_datetime(notification_date, notification_time)
        )
    except Exception:
        await message.answer(text=messages.DATETIME_FORMA_ERROR)

        await state.clear()
        await message.answer(text=messages.ENTER_TASK_NAME)
        await state.set_state(states.AddTask.name)

        return

    text = messages.CONFIRM_TASK_ADDING + messages.TASK_INFO_FORMATER.format(
        name, description, deadline_date, deadline_time, notification_date, notification_time
    )

    await message.answer(text=text, reply_markup=keyboards.confirm_task_adding)


@user.callback_query(F.data == "add_task")
async def confirm_task_adding(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    name = data["name"]
    description = data["description"]
    deadline = data["deadline"]
    notification = data["notification"]

    await state.clear()

    await callback.message.edit_reply_markup(reply_markup=None)

    try:
        await task_service.add_task(
            callback.from_user.id, name, description, deadline, notification
        )
    except Exception as ex:
        logger.error(f"{callback.from_user.id} could not add task: {ex}")
        return

    await callback.message.answer(
        text=messages.TASK_ADDED, reply_markup=keyboards.alltime_reply_keyboard
    )


@user.callback_query(F.data.startswith("page_task_"))
async def tasks_keyboard(callback: CallbackQuery, state: FSMContext):

    cur_page = int(callback.data.split("_")[-1])

    await state.clear()
    await callback.answer()

    kb = await keyboards.tasks_list_keyboard(cur_page, callback.from_user.id)

    await callback.message.edit_text(text=messages.CHOOSE_TASK, reply_markup=kb)


@user.callback_query(F.data.startswith("task_"))
async def show_task_info(callback: CallbackQuery, state: FSMContext):
    _, task_id, cur_page = callback.data.split("_")
    logger.debug(f"ask task with id:{task_id}")

    await callback.answer()

    task_info = await task_service.get_task(callback.from_user.id, task_id)

    logger.debug(f"before - {task_info}")

    text = await formaters.format_task_info(task_info)

    logger.debug(text)

    kb = await keyboards.task_info_keyboard(task_id=task_id, back_page=cur_page)

    await callback.message.edit_text(text=text, reply_markup=kb)


@user.callback_query(F.data.startswith("edit_task_"))
async def edit_task_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    _, _, field, task_id, back_page = callback.data.split("_")

    if field != "prolong":
        kb = await keyboards.task_edit_confirm(task_id=task_id, field=field, back_page=back_page)
        await callback.message.edit_text(text=messages.ACTION_CONFIRM, reply_markup=kb)
        return
    else:
        await callback.message.edit_text(text=messages.ENTER_NEW_DEADLINE_DATE, reply_markup=None)
        await state.clear()
        await state.update_data(task_id=task_id)
        await state.set_state(states.Prolong.deadline_date)


@user.message(states.Prolong.deadline_date)
async def task_edit_deadline_time(message: Message, state: FSMContext):
    await state.update_data(deadline_date=message.text)
    await message.answer(text=messages.ENTER_NEW_DEADLINE_TIME)
    await state.set_state(states.Prolong.deadline_time)


@user.message(states.Prolong.deadline_time)
async def task_edit_notification_date(message: Message, state: FSMContext):
    await state.update_data(deadline_time=message.text)
    await message.answer(text=messages.ENTER_NEW_NOTIFICATION_DATE)
    await state.set_state(states.Prolong.notification_date)


@user.message(states.Prolong.notification_date)
async def task_edit_notification_time(message: Message, state: FSMContext):
    await state.update_data(notification_date=message.text)
    await message.answer(text=messages.ENTER_NEW_NOTIFICATION_TIME)
    await state.set_state(states.Prolong.notification_time)


@user.message(states.Prolong.notification_time)
async def task_edit_show_fields(message: Message, state: FSMContext):
    await state.update_data(notification_time=message.text)

    data = await state.get_data()
    task_id = data["task_id"]
    deadline_date = data["deadline_date"]
    deadline_time = data["deadline_time"]
    notification_date = data["notification_date"]
    notification_time = data["notification_time"]

    try:
        await state.update_data(deadline=formaters.convert_datetime(deadline_date, deadline_time))
        await state.update_data(
            notification=formaters.convert_datetime(notification_date, notification_time)
        )
    except Exception:
        await message.answer(text=messages.DATETIME_FORMA_ERROR)

        await message.answer(text=messages.ENTER_NEW_DEADLINE_DATE, reply_markup=None)
        await state.clear()
        await state.update_data(task_id=task_id)
        await state.set_state(states.Prolong.deadline_date)

        return

    text = messages.TASK_AFTER_EDIT + messages.NEW_TIME.format(
        deadline_date, deadline_time, notification_date, notification_time
    )

    await message.answer(text=text)
    kb = await keyboards.task_edit_confirm(task_id=task_id, field="prolong", back_page=1)
    await message.answer(text=messages.ACTION_CONFIRM, reply_markup=kb)


@user.callback_query(F.data.startswith("confirm_edit_task_"))
async def confirm_task_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    _, _, _, field, task_id = callback.data.split("_")

    logger.debug(f"confirm - {field}")

    deadline = None
    notification = None
    data = await state.get_data()
    logger.debug(data)

    if field == "prolong":
        deadline = data["deadline"]
        notification = data["notification"]

    try:
        await task_service.edit_task(callback.from_user.id, task_id, field, deadline, notification)
        await callback.message.edit_text(text=messages.TASK_UPDATED, reply_markup=None)
        logger.debug(f"user {callback.from_user.id} ask tasks list")
        await state.clear()

        tasks = await task_service.get_tasks(callback.from_user.id)

        text = await formaters.format_tasks_list(tasks)

        await callback.message.answer(text=text, reply_markup=keyboards.under_tasks_list_keyboard)
    except Exception as ex:
        logger.error(f"{callback.from_user.id} could not edit task({task_id}): {ex}")
        return
