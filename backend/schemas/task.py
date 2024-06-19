from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.schemas.useful import Id


class TaskModel(Id):
    model_config = ConfigDict(from_attributes=True)

    start: datetime
    end: Union[datetime, None]
    timezone_offset: int
    name: str
    categories: list[str]


class TaskNameUpdate(Id):
    name: str
    forcibly: Optional[bool] = False


class TaskCreate(BaseModel):
    name: str
    forcibly: Optional[bool] = False


class TaskToCategory(BaseModel):
    category_id: UUID
    task_id: UUID
