from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.column import Column
from src.schemas.columns import ColumnCreate, ColumnUpdate


def get_column(db: Session, column_id: int) -> Column | None:
    return db.get(Column, column_id)


def get_all_columns(db: Session, project_id: int | None = None) -> list[Column]:
    q = db.query(Column)
    if project_id:
        q = q.filter(Column.project_id == project_id)
    return q.all()


def create_column(db: Session, data: ColumnCreate) -> Column:
    column_data = data.model_dump()
    
    # Calculate next position
    max_pos = db.query(func.max(Column.position)).filter(Column.project_id == data.project_id).scalar()
    column_data["position"] = (max_pos if max_pos is not None else -1) + 1

    obj = Column(**column_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def move_column(db: Session, column_id: int, new_position: int) -> Column | None:
    column = get_column(db, column_id)
    if not column:
        return None
    
    project_id = column.project_id
    old_position = column.position

    if old_position == new_position:
        return column
    
    if old_position < new_position:
        # Shift items down
        db.query(Column).filter(
            Column.project_id == project_id,
            Column.position > old_position,
            Column.position <= new_position
        ).update({Column.position: Column.position - 1}, synchronize_session=False)
    else:
        # Shift items up
        db.query(Column).filter(
            Column.project_id == project_id,
            Column.position >= new_position,
            Column.position < old_position
        ).update({Column.position: Column.position + 1}, synchronize_session=False)

    column.position = new_position
    db.commit()
    db.refresh(column)
    return column


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
