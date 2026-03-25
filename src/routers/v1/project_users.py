from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.project_users import get_project_user, get_all_project_users, create_project_user, update_project_user, delete_project_user
from src.schemas.project_users import ProjectUserCreate, ProjectUserOut, ProjectUserUpdate

router_project_users = APIRouter(
    prefix="/project-users", tags=["project-users"])


@router_project_users.get("/", response_model=List[ProjectUserOut])
def list_project_users(db: Session = Depends(get_db)):
    return get_all_project_users(db)


@router_project_users.get(
    "/{user_id}/{project_id}", response_model=ProjectUserOut
)
def read_project_user(
    user_id: int, project_id: int, db: Session = Depends(get_db)
):
    pu = get_project_user(db, user_id, project_id)
    if not pu:
        raise HTTPException(404, "Relation not found")
    return pu


@router_project_users.post("/", response_model=ProjectUserOut)
def create_pu(data: ProjectUserCreate, db: Session = Depends(get_db)):
    return create_project_user(db, data)


@router_project_users.put(
    "/{user_id}/{project_id}", response_model=ProjectUserOut
)
def update_pu(
    user_id: int,
    project_id: int,
    data: ProjectUserUpdate,
    db: Session = Depends(get_db)
):
    pu = update_project_user(db, user_id, project_id, data)
    if not pu:
        raise HTTPException(404, "Relation not found")
    return pu


@router_project_users.delete(
    "/{user_id}/{project_id}", response_model=ProjectUserOut
)
def delete_pu(
    user_id: int, project_id: int, db: Session = Depends(get_db)
):
    pu = delete_project_user(db, user_id, project_id)
    if not pu:
        raise HTTPException(404, "Relation not found")
    return pu
