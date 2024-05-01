import uuid

from pydantic import BaseModel


class Id(BaseModel):
    id: uuid.UUID
