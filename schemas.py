from pydantic import BaseModel
from typing import List
from datetime import date

# CLIENT
class ClientBase(BaseModel):
    name: str

class ClientDisplay(BaseModel):
    id: int
    name: str

# CATEGORY
class CategoryBase(BaseModel):
    name: str

class CategoryDisplay(BaseModel):
    id: int
    name: str

# CATEGORY CLIENT
class CatCliBase(BaseModel):
    client_id: int
    category_id: int
    
class CatCliDisplay(BaseModel):
    id: int
    client: ClientDisplay
    category: CategoryDisplay

# ACCOUNT
class AccountBase(BaseModel):
    client_id: int

class AccountDisplay(BaseModel):
    id: int
    client_id: int 

# GET CLIENT
class GetClient(BaseModel):
    client: ClientDisplay
    account: AccountDisplay
    category: CategoryDisplay

# MOVEMENT
class MovementBase(BaseModel):
    account_id: int
    transaction_type: str
    amount: float

class MovementDisplay(BaseModel):
    id: int
    account_id: int
    transaction_type: str
    amount: float
    date: date