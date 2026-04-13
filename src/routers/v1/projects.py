from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.projects import get_all_projects, get_project, create_project, update_project, delete_project, get_user_projects
from src.schemas.projects import ProjectCreate, ProjectOut, ProjectUpdate
from src.models.user import User
from src.core.services.auth_for_users import get_current_user_from_token

router_projects = APIRouter(prefix="/projects", tags=["projects"])


@router_projects.get("/", response_model=List[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    return get_user_projects(db, current_user.id)


@router_projects.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    pr = get_project(db, project_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Project not found")
    return pr


@router_projects.post("/", response_model=ProjectOut)
def create_project_endpoint(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    # Force created_by to be the current user
    data.created_by = current_user.id
    return create_project(db, data)


@router_projects.put("/{project_id}", response_model=ProjectOut)
def update_project_endpoint(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    pr = update_project(db, project_id, data)
    if not pr:
        raise HTTPException(status_code=404, detail="Project not found")
    return pr


@router_projects.delete("/{project_id}", response_model=ProjectOut)
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    pr = delete_project(db, project_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Project not found")
    return pr


@router_projects.post("/{project_id}/users", response_model=ProjectOut)
def add_user_to_project(
    project_id: int,
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    from src.crud.users import get_user_by_email
    from src.models.project_user import ProjectUser

    pr = get_project(db, project_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Project not found")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user already in project
    existing = db.query(ProjectUser).filter_by(
        project_id=project_id, user_id=user.id).first()
    if not existing:
        db.add(ProjectUser(project_id=project_id, user_id=user.id))
        db.commit()
        db.refresh(pr)

    return pr
