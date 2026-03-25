from sqlalchemy.orm import Session
from src.models.project_user import ProjectUser
from src.schemas.project_users import ProjectUserCreate, ProjectUserUpdate


def get_project_user(db: Session, user_id: int, project_id: int) -> ProjectUser | None:
    return db.query(ProjectUser).filter_by(user_id=user_id, project_id=project_id).first()


def get_all_project_users(db: Session) -> list[ProjectUser]:
    return db.query(ProjectUser).all()


def create_project_user(db: Session, data: ProjectUserCreate) -> ProjectUser:
    obj = ProjectUser(**data.model_dump())
    db.add(obj)
    db.commit()
    return obj


def update_project_user(db: Session, user_id: int, project_id: int, data: ProjectUserUpdate) -> ProjectUser | None:
    obj = get_project_user(db, user_id, project_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    return obj


def delete_project_user(db: Session, user_id: int, project_id: int) -> ProjectUser | None:
    obj = get_project_user(db, user_id, project_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
