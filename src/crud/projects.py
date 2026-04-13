from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.project import Project
from src.models.project_user import ProjectUser
from src.models.column import Column
from src.models.user import User
from src.schemas.projects import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def get_all_projects(db: Session) -> list[Project]:
    return db.query(Project).all()


def get_user_projects(db: Session, user_id: int) -> list[Project]:
    return db.query(Project).outerjoin(ProjectUser).filter(
        or_(
            Project.created_by == user_id,
            ProjectUser.user_id == user_id
        )
    ).distinct().all()


def create_project(db: Session, data: ProjectCreate) -> Project:
    project_data = data.model_dump(exclude={"columns", "member_emails"})
    obj = Project(**project_data)
    db.add(obj)
    db.flush()  # flush to get obj.id

    if data.columns:
        for idx, col_name in enumerate(data.columns):
            db.add(Column(project_id=obj.id, name=col_name, position=idx))

    # Add creator to project_user
    db.add(ProjectUser(project_id=obj.id, user_id=obj.created_by))

    if data.member_emails:
        users_to_add = db.query(User).filter(User.email.in_(data.member_emails)).all()
        for user in users_to_add:
            if user.id != obj.created_by: # Creator is usually owner, but consistency check
                db.add(ProjectUser(project_id=obj.id, user_id=user.id))

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
