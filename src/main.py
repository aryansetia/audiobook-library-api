from fastapi import FastAPI
from sqlalchemy.orm import Session
from src.database import engine, SessionLocal, Base
from src.routers import audiobook

app = FastAPI()

app.include_router(audiobook.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Application is up!"}