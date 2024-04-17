from fastapi import APIRouter, Depends
from schemas import ClientBase, ClientDisplay, CatCliBase, CatCliDisplay, GetClient
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_client
from typing import List

router = APIRouter(
    prefix='/client',
    tags=['client']
)

# CREATE CLIENT
@router.post('/', response_model=ClientDisplay)
def post_client(request: ClientBase, db: Session = Depends(get_db)):
    return db_client.post_client(db, request)

# GET ALL CLIENTS
@router.get('/all', response_model=List[ClientDisplay])
def get_all_clients(db: Session = Depends(get_db)):
    return db_client.get_all_clients(db)



# DELETE CLIENT
@router.delete('/{id}')
def delete_client(id: int, db: Session = Depends(get_db)):
    return db_client.delete_client(db, id)

#@router.post('/category')
#def create_category(name: str, db: Session = Depends(get_db)):
#    return db_client.create_category(db, name)


# POST CATEGORY CLIENT
@router.post('/cat_cli', response_model=CatCliDisplay)
def create_cat_cli(request: CatCliBase, db: Session = Depends(get_db)):
    return db_client.post_cat_cli(db, request)

@router.get('/{id}', response_model=GetClient)
def get_client(id: int, db: Session = Depends(get_db)):
    return db_client.get_full_client(db, id)
