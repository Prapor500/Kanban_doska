from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, Table
import datetime
from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    middle_name: Mapped[str] = mapped_column(String(128))
    gender: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))

    created_projects: Mapped[list["Project"]] = relationship(
        back_populates="creator")
    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee", foreign_keys="[Task.assigned_to]")
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="author", foreign_keys="[Task.created_by]")
    projects: Mapped[list["Project"]] = relationship(
        secondary="project_user", back_populates="users")
