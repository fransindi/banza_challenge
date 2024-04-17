from sqlalchemy.orm import Session
from schemas import ClientBase, CatCliBase
from .models import DbClient, DbCategory, DbCatCli, DbAccount
from fastapi import HTTPException, status


# GET CLIENT
def get_client(db: Session, id: int):
    return db.query(DbClient).filter(DbClient.id == id).first()

def get_client_by_name(db: Session, name: str):
    return db.query(DbClient).filter(DbClient.name == name).first()

# POST CLIENT
def post_client(db: Session, request: ClientBase):
    client = get_client_by_name(db, request.name)
    if not client:
        new_client = DbClient(
            name = request.name
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        new_account = DbAccount(
            client_id = new_client.id
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_client
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Client {request.name} already exists")

# GET ALL CLIENTS
def get_all_clients(db: Session):
    clients = db.query(DbClient).all()
    if not clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This db has no clients yet.")
    return clients

# DELETE CLIENT
def delete_client(db: Session, id: int):
    client = get_client(db, id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client with id {id} not found')
    db.delete(client)
    db.commit()
    return {
        'Client_id_deleted': id
    }

# CREATE CATEGORY
def create_category(db: Session, category_name: str):
    category = db.query(DbCategory).filter(DbCategory.name == category_name)
    if not category:
        new_category = DbCategory(
            name = category_name
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return 'Category correctly added'
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exist')

# POST CATEGORY CLIENT
def post_cat_cli(db: Session, request: CatCliBase):
    if request.category_id > 3 or request.category_id < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category id Not Found, try between 1 and 3')
    
    list_clients = get_client(db, request.client_id)
    if list_clients:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Client already exist')     

    new_cat_cli = DbCatCli(
        client_id = request.client_id,
        category_id = request.category_id
    )
    db.add(new_cat_cli)
    db.commit()
    db.refresh(new_cat_cli)
    return new_cat_cli

# GET CLIENT
def get_full_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client not Found')
    account = db.query(DbAccount).filter(DbAccount.client_id == client.id).first()
    id_cat_cli = db.query(DbCatCli).filter(DbCatCli.client_id == client.id).first()
    if not id_cat_cli:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    category = db.query(DbCategory).filter(DbCategory.id == id_cat_cli.category_id).first()
    

    return {
        'client': client,
        'account': account,
        'category': category
        }


