from task_service.logger import setup_logger
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
import uuid
from task_service.services.notification_service import publish_task_update


logger = setup_logger(__name__)


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "task_service")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
tasks_collection = db["tasks"]


async def create_indexes():
    await users_collection.create_index("tg_id", unique=True)
    await tasks_collection.create_index("tg_id")
    await tasks_collection.create_index("task_id", unique=True)


async def init_db():
    await create_indexes()


async def get_tasks_by_id(tg_id: str):
    try:
        tasks = await tasks_collection.find(
            {"tg_id": tg_id, "is_completed": {"$ne": True}},
            {"_id": 0, "created_at": 0},
        ).to_list(length=None)

        for task in tasks:
            task["deadline"] = task["deadline"].isoformat()
            task["notification"] = task["notification"].isoformat()

        return tasks
    except Exception as e:
        logger.error(e)
        return []


async def add_new_task_from_user(
    tg_id: str, name: str, description: str, deadline: str, notification: str
) -> str:
    try:
        user = await users_collection.find_one({"tg_id": tg_id})
        if not user:
            await users_collection.insert_one(
                {"tg_id": tg_id, "created_at": datetime.now().isoformat()}
            )

        deadline_dt = datetime.fromisoformat(deadline)
        notify_dt = datetime.fromisoformat(notification)

        task_id = str(uuid.uuid4())[:8]

        await tasks_collection.insert_one(
            {
                "task_id": task_id,
                "tg_id": tg_id,
                "name": name,
                "description": description,
                "deadline": deadline_dt,
                "notification": notify_dt,
                "created_at": datetime.now().isoformat(),
            }
        )

        await publish_task_update("add_new", task_id, tg_id, notify_dt)

        return "0"
    except Exception as e:
        logger.error(f"error in task creating: {str(e)}")
        return "1"


async def get_task_by_task_id(tg_id: str, task_id: str):
    try:
        task = await tasks_collection.find_one(
            {"tg_id": tg_id, "task_id": task_id},
            {"_id": 0, "created_at": 0},
        )

        if task:
            task["deadline"] = task["deadline"].isoformat()
            task["notification"] = task["notification"].isoformat()
            return task
        else:
            return {}
    except Exception as e:
        logger.error(f"error in get task: {str(e)}")
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
                            "updated_at": datetime.now().isoformat(),
                        }
                    },
                )

                await publish_task_update("edit", task_id, tg_id, notify_dt)

                return "0" if result.modified_count else "1"

            case "complete":
                result = await tasks_collection.update_one(
                    {"tg_id": tg_id, "task_id": task_id},
                    {
                        "$set": {
                            "is_completed": True,
                            "completed_at": datetime.now().isoformat(),
                        }
                    },
                )

                await publish_task_update("complete", task_id, tg_id)

                return "0" if result.modified_count else "1"

            case "delete":
                result = await tasks_collection.delete_one({"tg_id": tg_id, "task_id": task_id})

                await publish_task_update("delete", task_id, tg_id)

                return "0" if result.deleted_count else "1"

            case _:
                logger.warning(f"Unknown field: {field}")
                return "1"

    except Exception as e:
        logger.error(f"editing error: {e}")
        return "1"


async def add_user(tg_id: str) -> str:
    try:
        user = await users_collection.find_one({"tg_id": tg_id})
        if user:
            return "0"

        await users_collection.insert_one(
            {"tg_id": tg_id, "created_at": datetime.now().isoformat()}
        )
        return "0"
    except Exception as e:
        logger.error(f"error in user adding: {e}")
        return "1"


async def edit_task_text_by_task_id(tg_id: str, task_id, name: str, description: str):
    try:
        result = await tasks_collection.update_one(
            {"tg_id": tg_id, "task_id": task_id},
            {
                "$set": {
                    "name": name,
                    "description": description,
                    "updated_at": datetime.now().isoformat(),
                }
            },
        )

        return "0" if result.modified_count else "1"

    except Exception as e:
        logger.error(f"error in text editing: {e}")
        return "1"
