from fastapi import FastAPI
from router import client
from router import movement

from db import models
from db.database import engine

app = FastAPI()
app.include_router(client.router)
app.include_router(movement.router)




@app.get('/')
def hw():
    return "Hello World"

models.Base.metadata.create_all(engine)