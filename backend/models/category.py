from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.meta import Base, DEFAULT_SCHEMA
from backend.models.task import Task


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    tasks: Mapped[List[Task]] = relationship(
        'Task',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='categories',
    )
