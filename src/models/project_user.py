from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, Table
import datetime
from .base import Base


class ProjectUser(Base):
    __tablename__ = "project_user"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), primary_key=True)
