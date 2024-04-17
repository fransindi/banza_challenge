from sqlalchemy.orm import Session
from schemas import ClientBase, CatCliBase
from .models import DbClient, DbCategory, DbCatCli
from fastapi import HTTPException, status

def post_client(db: Session, request: ClientBase):
    new_client = DbClient(
        name = request.name
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

def get_all_clients(db: Session):
    return db.query(DbClient).all()

def get_client(db: Session, id: int):
    return db.query(DbClient).filter(DbClient.id == id).first()

def delete_client(db: Session, id: int):
    client = get_client(db, id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client with id {id} not found')
    db.delete(client)
    db.commit()
    return {
        'Client_id_deleted': id
    }

def create_category(db: Session, category_name: str):
    new_category = DbCategory(
        name = category_name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return 'Category correctly added'

def post_cat_cli(db: Session, request: CatCliBase):
    new_cat_cli = DbCatCli(
        client_id = request.client_id,
        category_id = request.category_id
    )
    db.add(new_cat_cli)
    db.commit()
    db.refresh(new_cat_cli)
    return new_cat_cli