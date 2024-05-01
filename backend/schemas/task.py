from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from time_management_bot.backend.schemas.useful import Id


class TaskModel(BaseModel):
    start: datetime
    end: datetime
    name: str


class TaskNameUpdate(Id):
    name: str
    forcibly: Optional[bool] = False


class TaskCreate(TaskModel):
    forcibly: Optional[bool] = False


class TaskToCategory(BaseModel):
    category_id: UUID
    task_id: UUID
