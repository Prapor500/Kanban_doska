from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.task import Task
from src.models.column import Column
from src.models.task_log import TaskLog
from src.models.user import User
from src.schemas.tasks import TaskCreate, TaskUpdate


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
            new_column = db.get(Column, new_column_id)
            if author and new_column:
                author_name = f"{author.first_name} {author.last_name}".strip() or author.email
                log = TaskLog(task_id=task_id, user_id=user_id, message=f"{author_name} переместил задачу в колонку \"{new_column.name}\"")
                db.add(log)

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

    if user_id:
        author = db.get(User, user_id)
        if author:
            author_name = f"{author.first_name} {author.last_name}".strip() or author.email
            
            if 'title' in updates and updates['title'] != obj.title:
                 log = TaskLog(task_id=task_id, user_id=user_id, message=f"{author_name} изменил название задачи")
                 db.add(log)

            if 'description' in updates and updates['description'] != obj.description:
                log = TaskLog(task_id=task_id, user_id=user_id, message=f"{author_name} изменил описание задачи")
                db.add(log)
            
            if 'column_id' in updates and updates['column_id'] != obj.column_id:
                 new_column = db.get(Column, updates['column_id'])
                 if new_column:
                     log = TaskLog(task_id=task_id, user_id=user_id, message=f"{author_name} переместил задачу в колонку \"{new_column.name}\"")
                     db.add(log)

            if 'assigned_to' in updates and updates['assigned_to'] != obj.assigned_to:
                new_assignee_id = updates['assigned_to']
                if new_assignee_id:
                    new_assignee = db.get(User, new_assignee_id)
                    if new_assignee:
                        assignee_name = f"{new_assignee.first_name} {new_assignee.last_name}".strip() or new_assignee.email
                        message = f"{author_name} передал задачу {assignee_name}"
                    else:
                         message = f"{author_name} изменил исполнителя"
                else:
                    message = f"{author_name} удалил исполнителя"
                
                log = TaskLog(task_id=task_id, user_id=user_id, message=message)
                db.add(log)

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
