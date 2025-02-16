from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    name = State()
    description = State()
    deadline_date = State()
    deadline_time = State()
    notification_date = State()
    notification_time = State()
