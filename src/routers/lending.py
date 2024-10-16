from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from datetime import datetime
from src.schemas.lending import LendingResponse, LendingCreate
from src.database import get_db
from src.models.user_account import User
from src.models.lending import Lending
from src.schemas.request_queue import RequestQueueResponse, RequestQueueCreate, RequestQueueListResponse
from src.models.audiobook import Audiobook
from src.authentication.auth import get_current_user
from datetime import timedelta
from pytz import utc
from typing import List, Optional

router = APIRouter()


@router.post("/lend", response_model=LendingResponse)
def lend_audiobook(audiobook_id: int = Query(..., description="ID of the audiobook to lend"), db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    audiobook = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()

    if not audiobook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audiobook not found")

    if not audiobook.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Audiobook is not available for lending")

    # Set the borrowed_at timestamp to current time (UTC)
    borrowed_at = datetime.now(utc)

    # Automatically set due_date to 7 days after borrowed_at
    due_date = borrowed_at + timedelta(days=7)

    # Create a new lending record
    new_lending = Lending(
        audiobook_id=audiobook_id,
        user_id=current_user.id,
        borrowed_at=borrowed_at,
        due_date=due_date,
        is_returned=False,
    )

    audiobook.is_available = False

    db.add(new_lending)
    db.commit()
    db.refresh(new_lending)

    return new_lending


@router.get("/lend/history", response_model=List[LendingResponse], status_code=status.HTTP_200_OK)
def get_lending_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lending_history = db.query(Lending).filter(Lending.user_id == current_user.id).all()

    if not lending_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No lending history found.")

    return lending_history
