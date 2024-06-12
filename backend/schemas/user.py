from pydantic import BaseModel


class TimezoneOffset(BaseModel):
    offset: int
