from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.projects import get_project, get_projects, create_project, update_project, delete_project
from src.schemas.projects import ProjectCreate, ProjectOut, ProjectUpdate

router_projects = APIRouter(prefix="/projects", tags=["projects"])


@router_projects.get("/", response_model=List[ProjectOut])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_projects(db, skip, limit)


@router_projects.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(
    data: ProjectCreate,
    db: Session = Depends(get_db)
):
    return create_project(db, data)


@router_projects.get("/{project_id}", response_model=ProjectOut)
def get_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db)
):
    proj = get_project(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router_projects.put("/{project_id}", response_model=ProjectOut)
def update_project_endpoint(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    proj = update_project(db, project_id, data)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router_projects.delete("/{project_id}", response_model=ProjectOut)
def delete_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db)
):
    proj = delete_project(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj
