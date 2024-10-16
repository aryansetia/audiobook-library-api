from fastapi import FastAPI
from sqlalchemy.sql.functions import user

from src.database import engine, Base
from src.routers import audiobook, user_account, lending, request_queue

app = FastAPI()

app.include_router(audiobook.router)
app.include_router(user_account.router)
app.include_router(lending.router)
app.include_router(request_queue.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Application is up!"}