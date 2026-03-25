from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.services.db import get_db
from src.crud.columns import (
    get_column, get_columns, create_column, update_column, delete_column)
from src.schemas.columns import ColumnCreate, ColumnOut, ColumnUpdate

router_columns = APIRouter(prefix="/columns", tags=["columns"])


@router_columns.get("/", response_model=List[ColumnOut])
def list_columns(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_columns(db, project_id, skip, limit)


@router_columns.post("/", response_model=ColumnOut, status_code=status.HTTP_201_CREATED)
def create_column_endpoint(
    data: ColumnCreate,
    db: Session = Depends(get_db)
):
    return create_column(db, data)


@router_columns.get("/{column_id}", response_model=ColumnOut)
def get_column_endpoint(
    column_id: int,
    db: Session = Depends(get_db)
):
    col = get_column(db, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col


@router_columns.put("/{column_id}", response_model=ColumnOut)
def update_column_endpoint(
    column_id: int,
    data: ColumnUpdate,
    db: Session = Depends(get_db)
):
    col = update_column(db, column_id, data)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col


@router_columns.delete("/{column_id}", response_model=ColumnOut)
def delete_column_endpoint(
    column_id: int,
    db: Session = Depends(get_db)
):
    col = delete_column(db, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col
