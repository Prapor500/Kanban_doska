import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.task import Task
from src.models.column import Column
from src.models.task_log import TaskLog
from src.models.user import User
from src.schemas.tasks import TaskCreate, TaskUpdate


def _add_log(db: Session, task_id: int, user_id: int, message: str) -> None:
    """Создаёт запись в журнале изменений задачи."""
    db.add(TaskLog(task_id=task_id, user_id=user_id, message=message))


def _moved_to_column_message(db: Session, author_name: str, column_id: int) -> str | None:
    """Формирует сообщение о перемещении задачи в колонку, либо None если колонка не найдена."""
    column = db.get(Column, column_id)
    if not column:
        return None
    return f"{author_name} переместил задачу в колонку \"{column.name}\""


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def get_all_tasks(db: Session, project_id: int | None = None) -> list[Task]:
    q = db.query(Task)
    if project_id:
        q = q.join(Column).filter(Column.project_id == project_id)
    return q.order_by(Task.position.asc()).all()


def create_task(db: Session, data: TaskCreate, user_id: int) -> Task:
    task_data = data.model_dump()
    task_data["created_by"] = user_id
    if task_data.get("assigned_to") is None:
        task_data["assigned_to"] = user_id
    
    # Calculate next position
    max_pos = db.query(func.max(Task.position)).filter(Task.column_id == data.column_id).scalar()
    task_data["position"] = (max_pos if max_pos is not None else -1) + 1

    obj = Task(**task_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def move_task(db: Session, task_id: int, new_column_id: int, new_position: int, user_id: int | None = None) -> Task | None:
    task = get_task(db, task_id)
    if not task:
        return None
    
    old_column_id = task.column_id
    old_position = task.position

    if old_column_id == new_column_id:
        if old_position == new_position:
            return task
        
        if old_position < new_position:
            # Shift items down (decrement index of items in between)
            db.query(Task).filter(
                Task.column_id == old_column_id,
                Task.position > old_position,
                Task.position <= new_position
            ).update({Task.position: Task.position - 1}, synchronize_session=False)
        else:
            # Shift items up (increment index of items in between)
            db.query(Task).filter(
                Task.column_id == old_column_id,
                Task.position >= new_position,
                Task.position < old_position
            ).update({Task.position: Task.position + 1}, synchronize_session=False)
    else:
        # Close gap in old column
        db.query(Task).filter(
            Task.column_id == old_column_id,
            Task.position > old_position
        ).update({Task.position: Task.position - 1}, synchronize_session=False)

        # Make room in new column
        db.query(Task).filter(
            Task.column_id == new_column_id,
            Task.position >= new_position
        ).update({Task.position: Task.position + 1}, synchronize_session=False)

        # Log column change
        if user_id:
            author = db.get(User, user_id)
            if author:
                message = _moved_to_column_message(db, author.display_name, new_column_id)
                if message:
                    _add_log(db, task_id, user_id, message)

    task.column_id = new_column_id
    task.position = new_position
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, user_id: int | None = None) -> Task | None:
    obj = get_task(db, task_id)
    if not obj:
        return None

    updates = data.model_dump(exclude_unset=True)

    if 'is_finished' in updates:
        if updates['is_finished'] and not obj.is_finished:
            updates['finished_at'] = datetime.datetime.now(datetime.UTC)
        elif not updates['is_finished']:
            updates['finished_at'] = None

    if user_id:
        author = db.get(User, user_id)
        if author:
            author_name = author.display_name
            
            if 'title' in updates and updates['title'] != obj.title:
                _add_log(db, task_id, user_id, f"{author_name} изменил название задачи")

            if 'description' in updates and updates['description'] != obj.description:
                _add_log(db, task_id, user_id, f"{author_name} изменил описание задачи")

            if 'column_id' in updates and updates['column_id'] != obj.column_id:
                message = _moved_to_column_message(db, author_name, updates['column_id'])
                if message:
                    _add_log(db, task_id, user_id, message)

            if 'assigned_to' in updates and updates['assigned_to'] != obj.assigned_to:
                new_assignee_id = updates['assigned_to']
                if new_assignee_id:
                    new_assignee = db.get(User, new_assignee_id)
                    if new_assignee:
                        message = f"{author_name} передал задачу {new_assignee.display_name}"
                    else:
                        message = f"{author_name} изменил исполнителя"
                else:
                    message = f"{author_name} удалил исполнителя"

                _add_log(db, task_id, user_id, message)

    for k, v in updates.items():
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
