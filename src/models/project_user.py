from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class ProjectUser(Base):
    __tablename__ = "project_user"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), primary_key=True)
