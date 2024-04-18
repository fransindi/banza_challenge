from fastapi import APIRouter, Depends, HTTPException
from schemas import MovementBase, MovementDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_movement
from typing import List


router = APIRouter(
    prefix='/movement',
    tags=['movement']
)

@router.post('/',
              response_model=MovementDisplay,
              summary='Create a new movement.',
              description='This Endpoint validate the user input and append a new line to the movement table in the database.',
              response_description='All the data posted in the database'
              )
def post_movement(request: MovementBase, db: Session = Depends(get_db)):
    return db_movement.post_movement(db, request)

@router.delete('/',
                summary='Delete a movement.',
                description='This endpoint look for a movement id and drop it from the table.',
                response_description='String with a text of confirmation in case is deleted or error in case dosent exist.'
                )
def delete_movement(id: int, db: Session = Depends(get_db)):
    return db_movement.delete_movement(db, id)

@router.get('/{id}',
             response_model=MovementDisplay,
             summary='Get the detail of a movement.',
             description='Retrieve from the database all the data from the movement in the database.',
             response_description='All the data from a specific movement.'
             )
def get_movement(id: int, db: Session = Depends(get_db)):
    return db_movement.get_movement_ep(db, id)

@router.get('/get_dolar_bolsa/',
             summary='get dolar bolsa price.',
             description='This endpoint hits the endpoint of dolarapi/dolar_bolsa and retrieve the selling price.',
             response_description='Dolar price in a Float type'
             )
def get_dolar():
    return db_movement.get_dolar_price()


@router.get('/total_usd/{account_id}',
            summary='Get the total of a user ARS converted to USD',
            description='This endpoint retrieve all the information from the movements of a client and calculates the total, then its multiplicated by the dolar bolsa sale price.',
            response_description='The total amount of the client in USD'
            )
def get_total_usd(account_id: int, db: Session = Depends(get_db)):
    return db_movement.get_total_usd(db, account_id)