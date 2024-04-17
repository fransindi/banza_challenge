from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    
class ClientDisplay(BaseModel):
    id: int
    name: str

class CategoryBase(BaseModel):
    name: str

class CategoryDisplay(BaseModel):
    id: int
    name: str

class CatCliBase(BaseModel):
    client_id: int
    category_id: int
    
class CatCliDisplay(BaseModel):
    id: int
    client: ClientDisplay
    category: CategoryDisplay