from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

from src.database import get_db
from src.schemas.audiobook import AudiobookCreate, AudiobookResponse, AudiobookUpdate
from src.models.audiobook import Audiobook

router = APIRouter()

@router.post("/audiobooks", response_model=AudiobookResponse, status_code=status.HTTP_201_CREATED)
def create_audiobook(audiobook: AudiobookCreate, db: Session = Depends(get_db)):
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
def get_audiobook(id: int, db: Session = Depends(get_db)):

    audiobook = db.query(Audiobook).filter(Audiobook.id == id).first()

    # If the audiobook is not found, raise a 404 error
    if audiobook is None:
        print(f"Audiobook with ID {id} not found.")  # Debugging print
        raise HTTPException(status_code=404, detail="Audiobook not found")


    # Return the audiobook details
    return audiobook

@router.put("/audiobooks/{id}", response_model=AudiobookResponse)
def update_audiobook(id: int, audiobook: AudiobookUpdate, db: Session = Depends(get_db)):
    db_audiobook = db.query(Audiobook).filter(Audiobook.id == id).first()

    if db_audiobook is None:
        raise HTTPException(status_code=404, detail="Audiobook not found")

    # Update the fields if they are provided in the request
    update_data = audiobook.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_audiobook, key, value)

    try:
        db.commit()
        db.refresh(db_audiobook)  # Refresh to get the updated instance
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e.orig)}")

    return db_audiobook
