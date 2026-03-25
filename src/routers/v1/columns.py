from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.core.services.db import get_db
from src.crud.columns import (
    get_all_columns, get_column, create_column, update_column, delete_column)
from src.schemas.columns import ColumnCreate, ColumnOut, ColumnUpdate

router_columns = APIRouter(prefix="/columns", tags=["columns"])


@router_columns.get("/", response_model=List[ColumnOut])
def list_columns(db: Session = Depends(get_db)):
    return get_all_columns(db)


@router_columns.get("/{column_id}", response_model=ColumnOut)
def read_column(column_id: int, db: Session = Depends(get_db)):
    col = get_column(db, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col


@router_columns.post("/", response_model=ColumnOut)
def create_column_endpoint(data: ColumnCreate, db: Session = Depends(get_db)):
    return create_column(db, data)


@router_columns.put("/{column_id}", response_model=ColumnOut)
def update_column_endpoint(column_id: int, data: ColumnUpdate, db: Session = Depends(get_db)):
    col = update_column(db, column_id, data)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col


@router_columns.delete("/{column_id}", response_model=ColumnOut)
def delete_column_endpoint(column_id: int, db: Session = Depends(get_db)):
    col = delete_column(db, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col
