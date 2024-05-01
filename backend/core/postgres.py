from typing import Any

from sqlalchemy import select, delete
from sqlalchemy.sql import and_
from sqlalchemy.orm import selectinload

from time_management_bot.backend.utils.exceptions import NotFoundException


class DBWork:

    def __init__(self, session):
        self.session = session

    @staticmethod
    async def get_filter(model, field_to_value: dict[str, Any]) -> list[bool]:
        return [getattr(model, attr) == value for attr, value in field_to_value.items()]

    async def get_obj(self, model, where: dict[str, Any] = None, field_for_load: str = None):
        query = select(model)
        if attr_for_load:
            query = query.options(selectinload(getattr(model, attr_for_load)))
        if where:
            query = query.filter(and_(*await self.get_filter(model, where)))
        return await self.session.scalars(query)

    async def create_obj(self, model, data_for_create: dict[str, Any]):
        obj = model(**data_for_create)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def delete_obj(self, model, where: dict[str, Any]) -> None:
        query = delete(model).where(and_(*await self.get_filter(model, where)))
        await self.session.execute(query)
        await self.session.commit()

    async def update_obj(self, model, where: dict, for_set: dict) -> None:
        obj = await self.get_obj(model, where)
        if not obj:
            raise NotFoundException(f'{model} object with {where.keys()} - {where.values()} does not exist')
        for attr, new_value in for_set.items():
            setattr(obj, attr, new_value)
        await self.session.commit()
