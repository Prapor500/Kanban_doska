from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.project_users import get_project_user, get_project_users, create_project_user, update_project_user, delete_project_user
from src.schemas.project_users import ProjectUserCreate, ProjectUserOut, ProjectUserUpdate

router_project_users = APIRouter(
    prefix="/project-users", tags=["project-users"])


@router_project_users.get("/", response_model=List[ProjectUserOut])
def list_project_users(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_project_users(db, project_id, skip, limit)


@router_project_users.post("/", response_model=ProjectUserOut, status_code=status.HTTP_201_CREATED)
def create_project_user_endpoint(
    data: ProjectUserCreate,
    db: Session = Depends(get_db)
):
    return create_project_user(db, data)


@router_project_users.get("/{pu_id}", response_model=ProjectUserOut)
def get_project_user_endpoint(
    pu_id: int,
    db: Session = Depends(get_db)
):
    pu = get_project_user(db, pu_id)
    if not pu:
        raise HTTPException(status_code=404, detail="ProjectUser not found")
    return pu


@router_project_users.put("/{pu_id}", response_model=ProjectUserOut)
def update_project_user_endpoint(
    pu_id: int,
    data: ProjectUserUpdate,
    db: Session = Depends(get_db)
):
    pu = update_project_user(db, pu_id, data)
    if not pu:
        raise HTTPException(status_code=404, detail="ProjectUser not found")
    return pu


@router_project_users.delete("/{pu_id}", response_model=ProjectUserOut)
def delete_project_user_endpoint(
    pu_id: int,
    db: Session = Depends(get_db)
):
    pu = delete_project_user(db, pu_id)
    if not pu:
        raise HTTPException(status_code=404, detail="ProjectUser not found")
    return pu
