from pydantic import BaseModel, ConfigDict


class TimezoneOffset(BaseModel):
    offset: int


class UserModel(BaseModel):
    chat_d: int
    id: int


class UserItems(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[UserModel]
