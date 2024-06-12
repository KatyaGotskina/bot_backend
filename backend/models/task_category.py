from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.meta import Base


class TaskCategory(Base):
    __tablename__ = 'task_to_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    task_id = mapped_column(Integer, ForeignKey('task.id'), nullable=False)
