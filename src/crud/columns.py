from sqlalchemy.orm import Session
from src.models.column import Column
from src.schemas.columns import ColumnCreate, ColumnUpdate


def get_column(db: Session, column_id: int) -> Column | None:
    return db.get(Column, column_id)


def get_all_columns(db: Session) -> list[Column]:
    return db.query(Column).all()


def create_column(db: Session, data: ColumnCreate) -> Column:
    obj = Column(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_column(db: Session, column_id: int, data: ColumnUpdate) -> Column | None:
    obj = get_column(db, column_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_column(db: Session, column_id: int) -> Column | None:
    obj = get_column(db, column_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
