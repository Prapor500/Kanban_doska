from sqlalchemy.orm import Session
from src.models.project import Project
from src.schemas.projects import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def get_all_projects(db: Session) -> list[Project]:
    return db.query(Project).all()


def create_project(db: Session, data: ProjectCreate) -> Project:
    obj = Project(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> Project | None:
    obj = get_project(db, project_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
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
