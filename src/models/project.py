from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, Table
import datetime
from .base import Base


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(255))

    creator: Mapped["User"] = relationship(back_populates="created_projects")
    columns: Mapped[list["Column"]] = relationship(back_populates="project")
    users: Mapped[list["User"]] = relationship(
        secondary="project_user", back_populates="projects")
