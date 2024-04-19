from sqlalchemy.orm import Session
from schemas import MovementBase
from .models import DbMovement, DbAccount
import datetime
from fastapi import HTTPException, status
from custom_log import log
import requests

# GET MOVEMENT FUNCTION
def get_movement(db: Session, id: int):
    movement = db.query(DbMovement).filter(DbMovement.id == id).first()
    if not movement:
        log('Get Movement', 'Movement not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movement not found')
    log('Get Movement', 'Movement retrieved')
    return movement

# POST MOVEMENT
def post_movement(db: Session, request: MovementBase):
    ingreso_egreso = ['ingreso', 'egreso']
    if request.transaction_type not in ingreso_egreso:
        log('Post Movement', 'Error, Not a valid transaction type')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid transaction type, try with ingreso or egreso')
    
    account = db.query(DbAccount).filter(DbAccount.id == request.account_id).first()

    if not account:
        log('Post Movement', 'Error, Inexistent account')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inexistent Account')
    
    if request.amount <= 0:
        log('Post Movement', 'Error, amount less than 0')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Input less than 0')
    
    if request.transaction_type == 'egreso':
        ars = get_total_ars(db, account.id)
        check_ars = ars - request.amount
        if check_ars < 0:
            log('Post Movement', 'Error, Cant witdraw more than your funds')
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
    log('Post Movement', 'Movement created.')
    return new_movement




# DELETE_MOVEMENT
def delete_movement(db: Session, id: int):
    movement = get_movement(db, id)
    if movement:
        db.delete(movement)
        db.commit()
        log('Delete Movement', 'Movement deleted.')
        return 'Deleted'
    log('Delete Movement', 'Movement doesnt exist.')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movement not found')

    

# GET MOVEMENT ENDPOINT
def get_movement_ep(db: Session, id: int):
    movement = get_movement(db, id)
    if not movement:
        log('Get Movement', 'Error, movement doesnt exist.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movement Not Found')
    log('Get Movement', 'Movement retrieved.')
    return movement


def get_dolar_price():
    url = "https://dolarapi.com/v1/dolares/bolsa"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        log('Get Dolar Price', 'Dolar Price Retrieved')
        return data['venta']
    else:
        log('Get Dolar Price', 'Error, no response from API')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No response from api')



def get_total_ars(db: Session, account_id: int):
    account = db.query(DbMovement).filter(DbMovement.account_id == account_id).all()
    if not account:
        log('Get Total ARS', 'Inexistent Account')
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
            log('Get Total ARS', 'Invalid transaction type')
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='transaction_type is not ingreso or egreso')
        
    ingresos = sum(ingresos)
    egresos = sum(egresos)
    pesos = ingresos - egresos
    log('Get Total ARS', 'ARS Retrieved')
    return pesos

def get_total_usd(db: Session, account_id: int):
    pesos = get_total_ars(db, account_id)
    if pesos < 0:
        log('Get Total USD', 'Funds Lower than 0')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Funds lower than 0')
    
    usd_price = get_dolar_price()
    final_usd = round((pesos / usd_price), 2)
    log('Get Total USD', 'USD Retrieved')
    return {
        'total_usd': final_usd
    }


