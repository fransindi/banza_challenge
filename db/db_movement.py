from sqlalchemy.orm import Session
from schemas import MovementBase
from .models import DbMovement, DbAccount
import datetime
from fastapi import HTTPException, status
import requests


def post_movement(db: Session, request: MovementBase):
    ingreso_egreso = ['ingreso', 'egreso']
    if request.transaction_type not in ingreso_egreso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid transaction type, try with Ingreso or Egreso')
    
    account = db.query(DbAccount).filter(DbAccount.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inexistent Account')
    
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Input less than 0')
    
    new_movement = DbMovement(
        account_id = request.account_id,
        transaction_type = request.transaction_type,
        amount = request.amount,
        date = datetime.date.today()
    )
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_movement


def get_movement(db: Session, id: int):
    return db.query(DbMovement).filter(DbMovement.id == id).first()
    

def delete_movement(db: Session, id: int):
    movement = get_movement(db, id)
    if not movement:
        db.delete(movement)
        db.commit()
        return 'Deleted'
    

def get_movement_ep(db: Session, id: int):
    movement = get_movement(db, id)
    if not movement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movement Not Found')
    return movement


def get_valor_dolar():
    url = "https://dolarapi.com/v1/dolares/bolsa"
    data = requests.get(url)
    if data.status_code == 200:
        return data.json()
