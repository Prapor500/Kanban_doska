from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey, Table
import datetime
from .base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    column_id: Mapped[int] = mapped_column(ForeignKey("column.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True)

    column: Mapped["Column"] = relationship(back_populates="tasks")
    author: Mapped["User"] = relationship(
        foreign_keys=[created_by], back_populates="created_tasks")
    assignee: Mapped["User"] = relationship(
        foreign_keys=[assigned_to], back_populates="assigned_tasks")
    logs: Mapped[list["TaskLog"]] = relationship(back_populates="task")
