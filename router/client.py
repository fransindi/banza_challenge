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
@router.post('/',
              response_model=ClientDisplay,
              summary='Create a new client',
              description='This Endpoint create a new client and a new account linked with the client.',
              response_description='All the data from the client created.'
              )
def post_client(request: ClientBase, db: Session = Depends(get_db)):
    return db_client.post_client(db, request)

# GET ALL CLIENTS
@router.get('/all',
             response_model=List[ClientDisplay],
             summary='Retrieve all clients',
             description='This Endpoint calls for all the clients in our database',
             response_description='List of all the clients in our database.'
             )
def get_all_clients(db: Session = Depends(get_db)):
    return db_client.get_all_clients(db)



# DELETE CLIENT
@router.delete('/{id}',
               summary='Delete a client',
               description='Insert the id of an existing client and this will be removed.',
               response_description='A string of confirmation in case is deleted, an error message in case of the client doesnt exist.'
               )
def delete_client(id: int, db: Session = Depends(get_db)):
    return db_client.delete_client(db, id)

@router.post('/category')
def create_category(name: str, db: Session = Depends(get_db)):
    return db_client.create_category(db, name)


# POST CATEGORY CLIENT
@router.post('/cat_cli',
              response_model=CatCliDisplay,
              summary='Link a client with a category.',
              description='Insert a client_id and a category_id and link this two in a relation table.',
              response_description='The data of the new line in the database.'
             )
def create_cat_cli(request: CatCliBase, db: Session = Depends(get_db)):
    return db_client.post_cat_cli(db, request)

@router.get('/{id}',
             response_model=GetClient,
             summary='Get full data of a client.',
             description='Insert an client id and retrieve information about a client, their accounts and categories.',
             response_description='Json format from the client, accounts and categories.'
             )
def get_client(id: int, db: Session = Depends(get_db)):
    return db_client.get_full_client(db, id)
