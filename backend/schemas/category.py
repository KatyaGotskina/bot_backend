from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from time_management_bot.backend.schemas.useful import Id


class CategoryModel(Id):
    name: str


class CategoryCreate(BaseModel):
    name: str
