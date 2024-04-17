from sqlalchemy.orm import Session
from schemas import ClientBase
from .models import DbClient

def create_client(db: Session, request: ClientBase):
    new_client = DbClient(
        name = request.name
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client