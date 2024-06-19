from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.meta import Base, DEFAULT_SCHEMA

if TYPE_CHECKING:
    from backend.models.category import Category


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    end: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone_offset: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    name: Mapped[str] = mapped_column(String)
    categories: Mapped[List['Category']] = relationship(
        'Category',
        secondary=f'{DEFAULT_SCHEMA}.task_to_category',
        back_populates='tasks',
    )
