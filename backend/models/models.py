from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.meta import Base, DEFAULT_SCHEMA


class UUIDMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class User(Base, UUIDMixin):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String, unique=True)
    code: Mapped[str] = mapped_column(String)


class Task(Base, UUIDMixin):
    __tablename__ = 'task'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)  # NOTE
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    end: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(String)
    categories: Mapped[List['Category']] = relationship(
        'Category',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='tasks',
    )


class Category(Base, UUIDMixin):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column(String)
    tasks: Mapped[List[Task]] = relationship(
        'Task',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='categories',
    )


class TaskCategory(Base, UUIDMixin):
    __tablename__ = 'task_to_category'

    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    task_id = mapped_column(Integer, ForeignKey('task.id'), nullable=False)
