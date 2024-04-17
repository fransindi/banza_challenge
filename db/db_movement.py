from sqlalchemy.orm import Session
from schemas import MovementBase
from .models import DbMovement, DbAccount
import datetime
from fastapi import HTTPException, status

def post_movement(db: Session, request: MovementBase):
    ingreso_egreso = ['ingreso', 'egreso']
    if request.transaction_type not in ingreso_egreso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid transaction type, try with Ingreso or Egreso')
    
    account = db.query(DbAccount).filter(DbAccount.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inexistent Account')
    
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