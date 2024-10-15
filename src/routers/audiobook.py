from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

from src.database import get_db
from src.schemas.audiobook import AudiobookCreate, AudiobookResponse, AudiobookUpdate
from src.models.audiobook import Audiobook
from src.models.user_account import User
from src.authentication.auth import get_current_user

router = APIRouter()


@router.post("/audiobooks", response_model=AudiobookResponse, status_code=status.HTTP_201_CREATED)
def create_audiobook(audiobook: AudiobookCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    db_audiobook = Audiobook(
        title=audiobook.title,
        author=audiobook.author,
        duration=audiobook.duration,
        cover_image_url=audiobook.cover_image_url,
    )

    try:
        db.add(db_audiobook)
        db.commit()
        response_data = {
            "message": "Audiobook created successfully",
        }
        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/audiobooks/{id}", response_model=AudiobookResponse)
def get_audiobook(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    audiobook = db.query(Audiobook).filter(Audiobook.id == id).first()

    if audiobook is None:
        raise HTTPException(status_code=404, detail="Audiobook not found")

    return audiobook


@router.put("/audiobooks/{id}", response_model=AudiobookResponse)
def update_audiobook(id: int, audiobook: AudiobookUpdate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    db_audiobook = db.query(Audiobook).filter(Audiobook.id == id).first()

    if db_audiobook is None:
        raise HTTPException(status_code=404, detail="Audiobook not found")

    update_data = audiobook.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_audiobook, key, value)

    try:
        db.commit()
        db.refresh(db_audiobook)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e.orig)}")

    return db_audiobook


@router.delete("/audiobooks/{id}", status_code=status.HTTP_200_OK)
def delete_audiobook(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_audiobook = db.query(Audiobook).filter(Audiobook.id == id).first()

    if db_audiobook is None:
        raise HTTPException(status_code=404, detail="Audiobook not found")

    try:
        db.delete(db_audiobook)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Audiobook deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
