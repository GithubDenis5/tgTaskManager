from task_service.logger import setup_logger
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
import uuid

logger = setup_logger(__name__)


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "task_service")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
tasks_collection = db["tasks"]


async def create_indexes():
    # Создаем уникальный индекс для tg_id в пользователе
    await users_collection.create_index("tg_id", unique=True)
    # Индексы для задач
    await tasks_collection.create_index("tg_id")
    await tasks_collection.create_index("task_id", unique=True)


async def init_db():
    await create_indexes()


async def get_tasks_by_id(tg_id: str):
    try:
        # Добавляем фильтр по is_completed
        tasks = await tasks_collection.find(
            {"tg_id": tg_id, "is_completed": {"$ne": True}},  # Только невыполненные
            {"_id": 0, "created_at": 0},
        ).to_list(length=None)

        for task in tasks:
            # Конвертация дат, как раньше
            task["deadline"] = task["deadline"].isoformat()
            task["notification"] = task["notification"].isoformat()

        return tasks
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return []


async def add_new_task_from_user(
    tg_id: str, name: str, description: str, deadline: str, notification: str
) -> str:
    try:
        # Проверка существования пользователя
        user = await users_collection.find_one({"tg_id": tg_id})
        if not user:
            await users_collection.insert_one(
                {"tg_id": tg_id, "created_at": datetime.utcnow().isoformat()}
            )

        # Парсинг дат
        deadline_dt = datetime.fromisoformat(deadline)
        notify_dt = datetime.fromisoformat(notification)

        # Генерация task_id
        task_id = str(uuid.uuid4())[:8]

        # Вставка в БД (даты сохраняем как datetime)
        await tasks_collection.insert_one(
            {
                "task_id": task_id,
                "tg_id": tg_id,
                "name": name,
                "description": description,
                "deadline": deadline_dt,
                "notification": notify_dt,
                "created_at": datetime.utcnow().isoformat(),
            }
        )

        return "0"
    except Exception as e:
        logger.error(f"Ошибка создания задачи: {str(e)}")
        return "1"


async def get_task_by_task_id(tg_id: str, task_id: str):
    try:
        task = await tasks_collection.find_one(
            {"tg_id": tg_id, "task_id": task_id},
            {"_id": 0, "created_at": 0},  # Исключаем служебные поля
        )

        if task:
            # Преобразуем даты в строки ISO формата
            task["deadline"] = task["deadline"].isoformat()
            task["notification"] = task["notification"].isoformat()
            return task
        else:
            return {}  # Задача не найдена
    except Exception as e:
        logger.error(f"Ошибка получения задачи: {str(e)}")
        return {}


async def edit_task_by_task_id(
    tg_id: str, task_id: str, field: str, new_deadline: str, new_notification: str
) -> str:
    try:
        match field:
            case "prolong":
                deadline_dt = datetime.fromisoformat(new_deadline)
                notify_dt = datetime.fromisoformat(new_notification)

                result = await tasks_collection.update_one(
                    {"tg_id": tg_id, "task_id": task_id},
                    {
                        "$set": {
                            "deadline": deadline_dt,
                            "notification": notify_dt,
                            "updated_at": datetime.utcnow().isoformat(),
                        }
                    },
                )
                return "0" if result.modified_count else "1"

            case "complete":
                # Помечаем задачу как завершенную
                result = await tasks_collection.update_one(
                    {"tg_id": tg_id, "task_id": task_id},
                    {
                        "$set": {
                            "is_completed": True,
                            "completed_at": datetime.utcnow().isoformat(),
                        }
                    },
                )
                return "0" if result.modified_count else "1"

            case "delete":
                # Удаляем задачу
                result = await tasks_collection.delete_one({"tg_id": tg_id, "task_id": task_id})
                return "0" if result.deleted_count else "1"

            case _:
                # Несуществующее действие
                logger.warning(f"Unknown field: {field}")
                return "1"

    except Exception as e:
        logger.error(f"Ошибка редактирования задачи: {str(e)}")
        return "1"

    except Exception as e:
        logger.error(f"Ошибка редактирования: {e}")
        return "1"


async def add_user(tg_id: str) -> str:
    try:
        user = await users_collection.find_one({"tg_id": tg_id})
        if user:
            return "0"  # Пользователь уже существует

        await users_collection.insert_one({"tg_id": tg_id, "created_at": datetime.isoformat()})
        return "0"
    except Exception as e:
        logger.error(f"Ошибка добавления пользователя: {e}")
        return "1"


# async def get_tasks_by_id(tg_id: int):
#     result = [
#         {
#             "task_id": "abc123",
#             "name": "Отчет",
#             "description": "Сделать отчет",
#             "deadline": "2025-02-20T18:00:00",
#             "notification": "2025-02-19T10:00:00",
#         },
#         {
#             "task_id": "xyz789",
#             "name": "Презентация",
#             "description": "Подготовить презентацию",
#             "deadline": "2025-02-22T15:00:00",
#             "notification": "2025-02-21T09:00:00",
#         },
#     ]

#     return result


# async def add_new_task_from_user(
#     tg_id: int, name: str, description: str, deadline: str, notification: str
# ):

#     # усли нет ошибки, то возвращаем 0, иначе 1

#     return "0"


# async def get_task_by_task_id(tg_id: int, task_id: str):
#     result = [
#         {
#             "task_id": "abc123",
#             "name": "Отчет",
#             "description": "Сделать отчет",
#             "deadline": "2025-02-20T18:00:00",
#             "notification": "2025-02-19T10:00:00",
#         },
#         {
#             "task_id": "xyz789",
#             "name": "Презентация",
#             "description": "Подготовить презентацию",
#             "deadline": "2025-02-22T15:00:00",
#             "notification": "2025-02-21T09:00:00",
#         },
#     ]
#     if task_id == "abc123":
#         return result[0]
#     elif task_id == "xyz789":
#         return result[1]


# async def edit_task_by_task_id(tg_id, task_id, field, deadline, notification):

#     # усли нет ошибки, то возвращаем 0, иначе 1

#     return "0"


# async def add_user(tg_id: int):

#     return "0"
