from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.meta import Base, DEFAULT_SCHEMA


class UUIDMixin(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class User(UUIDMixin):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String, unique=True)
    code: Mapped[str] = mapped_column(String)


class Task(UUIDMixin):
    __tablename__ = 'task'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)  # NOTE
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    end: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(String)


class Category(UUIDMixin):
    __table_name__ = 'category'

    name: Mapped[str] = mapped_column(String)


class TaskCategory(UUIDMixin):
    __tablename__ = 'task_to_category'

    category_id = mapped_column(Integer, ForeignKey('category.id', nullable=False))
    task_id = mapped_column(Integer, ForeignKey('task.id', nullable=False))
