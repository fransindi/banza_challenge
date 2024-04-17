from fastapi import APIRouter, Depends
from schemas import MovementBase
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_movement
from typing import List

router = APIRouter(
    prefix='/movement',
    tags=['movement']
)

@router.post('/')
def post_movement(request: MovementBase, db: Session = Depends(get_db)):
    return db_movement.post_movement(db, request)
