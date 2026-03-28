from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base


class Column(Base):
    __tablename__ = "column"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    name: Mapped[str] = mapped_column(String(255))
    position: Mapped[int]

    project: Mapped["Project"] = relationship(back_populates="columns")
    tasks: Mapped[list["Task"]] = relationship(back_populates="column")
