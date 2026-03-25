from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.projects import get_all_projects, get_project, create_project, update_project, delete_project
from src.schemas.projects import ProjectCreate, ProjectOut, ProjectUpdate

router_projects = APIRouter(prefix="/projects", tags=["projects"])


@router_projects.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return get_all_projects(db)


@router_projects.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    pr = get_project(db, project_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Project not found")
    return pr


@router_projects.post("/", response_model=ProjectOut)
def create_project_endpoint(data: ProjectCreate, db: Session = Depends(get_db)):
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
