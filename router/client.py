from fastapi import APIRouter, Depends
from schemas import ClientBase
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_client

router = APIRouter(
    prefix='/client',
    tags=['client']
)


@router.post('/')
def create_client(request: ClientBase, db: Session = Depends(get_db)):
    return db_client.create_client(db, request)