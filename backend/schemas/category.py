from pydantic import BaseModel

from backend.schemas.useful import Id


class CategoryModel(Id):
    name: str


class CategoryCreate(BaseModel):
    name: str
