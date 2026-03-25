from sqlalchemy.orm import Session
from src.models.project import Project
from src.schemas.projects import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, data: ProjectCreate) -> Project:
    obj = Project(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_project(db: Session, project_id: int, updates: ProjectUpdate) -> Project | None:
    obj = get_project(db, project_id)
    if not obj:
        return None
    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(obj, field, val)
    db.commit()
    db.refresh(obj)
    return obj


def delete_project(db: Session, project_id: int) -> Project | None:
    obj = get_project(db, project_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
