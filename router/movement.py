from fastapi import APIRouter, Depends, HTTPException
from schemas import MovementBase, MovementDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_movement
from typing import List


router = APIRouter(
    prefix='/movement',
    tags=['movement']
)

@router.post('/', response_model=MovementDisplay)
def post_movement(request: MovementBase, db: Session = Depends(get_db)):
    return db_movement.post_movement(db, request)

@router.delete('/')
def delete_movement(id: int, db: Session = Depends(get_db)):
    return db_movement.delete_movement(db, id)

@router.get('/{id}', response_model=MovementDisplay)
def get_movement(id: int, db: Session = Depends(get_db)):
    return db_movement.get_movement_ep(db, id)

@router.get('/nidea/')
def get_dolar():
    return db_movement.get_valor_dolar()