from sqlalchemy.orm import Session
from src.models.task import Task
from src.schemas.tasks import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()


def create_task(db: Session, data: TaskCreate) -> Task:
    obj = Task(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task | None:
    obj = get_task(db, task_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_task(db: Session, task_id: int) -> Task | None:
    obj = get_task(db, task_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
