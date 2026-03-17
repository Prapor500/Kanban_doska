from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, Table
import datetime
from .base import Base


class Column(Base):
    __tablename__ = "column"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    name: Mapped[str] = mapped_column(String(255))
    position: Mapped[int]

    project: Mapped["Project"] = relationship(back_populates="project_column")
    tasks: Mapped[list["Task"]] = relationship(back_populates="task_column")
