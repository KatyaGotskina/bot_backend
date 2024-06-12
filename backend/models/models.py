from typing import List

from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.meta import Base, DEFAULT_SCHEMA


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class User(Base, IdMixin):
    __tablename__ = 'user'

    timezone_offset: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Task(Base, IdMixin):
    __tablename__ = 'task'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    end: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    name: Mapped[str] = mapped_column(String)
    categories: Mapped[List['Category']] = relationship(
        'Category',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='tasks',
    )


class Category(Base, IdMixin):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column(String)
    tasks: Mapped[List[Task]] = relationship(
        'Task',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='categories',
    )


class TaskCategory(Base, IdMixin):
    __tablename__ = 'task_to_category'

    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    task_id = mapped_column(Integer, ForeignKey('task.id'), nullable=False)
