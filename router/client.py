from fastapi import APIRouter, Depends
from schemas import ClientBase, ClientDisplay, CatCliBase, CatCliDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_client
from typing import List

router = APIRouter(
    prefix='/client',
    tags=['client']
)


@router.post('/', response_model=ClientDisplay)
def post_client(request: ClientBase, db: Session = Depends(get_db)):
    return db_client.post_client(db, request)

@router.get('/all', response_model=List[ClientDisplay])
def get_all_clients(db: Session = Depends(get_db)):
    return db_client.get_all_clients(db)

@router.get('/{id}', response_model=ClientDisplay)
def get_client(id: int, db: Session = Depends(get_db)):
    return db_client.get_client(db, id)

@router.delete('/{id}')
def delete_client(id: int, db: Session = Depends(get_db)):
    return db_client.delete_client(db, id)

#@router.post('/category')
#def create_category(name: str, db: Session = Depends(get_db)):
 #   return db_client.create_category(db, name)

@router.post('/cat_cli', response_model=CatCliDisplay)
def create_cat_cli(request: CatCliBase, db: Session = Depends(get_db)):
    return db_client.post_cat_cli(db, request)

