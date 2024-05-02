import uuid

from pydantic import BaseModel


class Id(BaseModel):
    id: int
