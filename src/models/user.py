from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))

    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(128), nullable=True)
    gender: Mapped[str] = mapped_column(String(128), nullable=True)

    created_projects: Mapped[list["Project"]] = relationship(
        back_populates="creator")
    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee", foreign_keys="[Task.assigned_to]")
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="author", foreign_keys="[Task.created_by]")
    projects: Mapped[list["Project"]] = relationship(
        secondary="project_user", back_populates="users")
