from sqlalchemy.orm import Session
from schemas import MovementBase
from .models import DbMovement, DbAccount
import datetime
from fastapi import HTTPException, status
import requests

# GET MOVEMENT FUNCTION
def get_movement(db: Session, id: int):
    return db.query(DbMovement).filter(DbMovement.id == id).first()
    
# POST MOVEMENT
def post_movement(db: Session, request: MovementBase):
    ingreso_egreso = ['ingreso', 'egreso']
    if request.transaction_type not in ingreso_egreso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid transaction type, try with Ingreso or Egreso')
    
    account = db.query(DbAccount).filter(DbAccount.id == request.account_id).first()

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inexistent Account')
    
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Input less than 0')
    
    ars = get_total_pesos(db, account.id)
    check_ars = ars - request.amount
    if check_ars < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You dont have enough funds')

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




# DELETE_MOVEMENT
def delete_movement(db: Session, id: int):
    movement = get_movement(db, id)
    if not movement:
        db.delete(movement)
        db.commit()
        return 'Deleted'
    
# GET MOVEMENT ENDPOINT
def get_movement_ep(db: Session, id: int):
    movement = get_movement(db, id)
    if not movement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movement Not Found')
    return movement


def get_dolar_price():
    url = "https://dolarapi.com/v1/dolares/bolsa"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        return data['compra']
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No response from api')



def get_total_pesos(db: Session, account_id: int):
    account = db.query(DbMovement).filter(DbMovement.account_id == account_id).all()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No account with this id')
    ingresos = []
    egresos = []
    for move in account:
        if move.transaction_type == 'ingreso':
            ingresos.append(move.amount)
            continue
        elif move.transaction_type == 'egreso':
            egresos.append(move.amount)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='transaction_type is not ingreso or egreso')
        
    ingresos = sum(ingresos)
    egresos = sum(egresos)
    pesos = ingresos - egresos
    return pesos

def get_total_usd(db: Session, account_id: int):
    pesos = get_total_pesos(db, account_id)
    if pesos < 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Funds lower than 0')
    
    usd_price = get_dolar_price()
    final_usd = round((pesos / usd_price), 2)
    return {
        'total_usd': final_usd
    }


