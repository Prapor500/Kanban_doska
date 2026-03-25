from sqlalchemy.orm import Session
from src.models.project_user import ProjectUser
from src.schemas.project_users import ProjectUserCreate, ProjectUserUpdate


def get_project_user(db: Session, pu_id: int) -> ProjectUser | None:
    return db.query(ProjectUser).filter(ProjectUser.id == pu_id).first()


def get_project_users(db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[ProjectUser]:
    return (
        db.query(ProjectUser)
          .filter(ProjectUser.project_id == project_id)
          .offset(skip)
          .limit(limit)
          .all()
    )


def create_project_user(db: Session, data: ProjectUserCreate) -> ProjectUser:
    pu = ProjectUser(**data.model_dump())
    db.add(pu)
    db.commit()
    db.refresh(pu)
    return pu


def update_project_user(db: Session, pu_id: int, updates: ProjectUserUpdate) -> ProjectUser | None:
    pu = get_project_user(db, pu_id)
    if not pu:
        return None
    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(pu, field, val)
    db.commit()
    db.refresh(pu)
    return pu


def delete_project_user(db: Session, pu_id: int) -> ProjectUser | None:
    pu = get_project_user(db, pu_id)
    if not pu:
        return None
    db.delete(pu)
    db.commit()
    return pu
