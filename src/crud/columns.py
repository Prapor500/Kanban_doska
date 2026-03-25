from sqlalchemy.orm import Session
from src.models.column import Column
from src.schemas.columns import ColumnCreate, ColumnUpdate


def get_column(db: Session, column_id: int) -> Column | None:
    return db.query(Column).filter(Column.id == column_id).first()


def get_columns(db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[Column]:
    return (
        db.query(Column)
          .filter(Column.project_id == project_id)
          .order_by(Column.position)
          .offset(skip)
          .limit(limit)
          .all()
    )


def create_column(db: Session, data: ColumnCreate) -> Column:
    obj = Column(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_column(db: Session, column_id: int, updates: ColumnUpdate) -> Column | None:
    obj = get_column(db, column_id)
    if not obj:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
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
