from collections import deque
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
from src.database import get_db
from src.models.user_account import User
from src.schemas.request_queue import RequestQueueResponse
from src.models.audiobook import Audiobook
from src.authentication.auth import get_current_user
from pytz import utc
from src.models.request_queue import RequestQueue

router = APIRouter()


class RequestQueueManager:
    queues = {}

    def add_to_queue(self, audiobook_id: int, user_id: str):
        if audiobook_id not in self.queues:
            self.queues[audiobook_id] = deque()
        self.queues[audiobook_id].append(user_id)

    def remove_from_queue(self, audiobook_id: int):
        if audiobook_id in self.queues and self.queues[audiobook_id]:
            return self.queues[audiobook_id].popleft()
        return None

    def get_queue(self, audiobook_id: int):
        return list(self.queues.get(audiobook_id, deque()))

    def is_queue_empty(self, audiobook_id: int):
        return len(self.queues.get(audiobook_id, deque())) == 0


q_manager = RequestQueueManager()


@router.post("/lend/request", response_model=RequestQueueResponse)
def request_audiobook(audiobook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    audiobook = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()

    if audiobook is None or audiobook.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audiobook is currently available or does not exist"
        )

    # Check if the user is already in the request queue
    queue = q_manager.get_queue(audiobook_id)
    if current_user.email in queue:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already requested this audiobook and are in the queue."
        )

    q_manager.add_to_queue(audiobook_id, current_user.email)

    print(f"User {current_user.username} added to the queue for audiobook '{audiobook.title}'.")

    new_request = RequestQueue(
        audiobook_id=audiobook_id,
        user_id=current_user.id,
        request_date=datetime.now(utc)
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return RequestQueueResponse(
        id=new_request.id,
        audiobook_id=new_request.audiobook_id,
        user_id=new_request.user_id,
        request_date=new_request.request_date
    )


@router.get("/lend/queue/{audiobook_id}", response_model=list[str])
def get_audiobook_queue(audiobook_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    audiobook = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()

    if not audiobook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook does not exist"
        )

    queue = q_manager.get_queue(audiobook_id)

    print(f"Queue for audiobook '{audiobook.title}' retrieved: {queue}")

    return queue


@router.post("/lend/return", status_code=status.HTTP_200_OK)
def return_audiobook(
    audiobook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audiobook = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()

    if audiobook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audiobook not found"
        )

    user_request = db.query(RequestQueue).filter(
        RequestQueue.audiobook_id == audiobook_id,
        RequestQueue.user_id == current_user.id
    ).first()

    if user_request is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to return this audiobook"
        )

    if not q_manager.is_queue_empty(audiobook_id):
        next_user_id = q_manager.remove_from_queue(audiobook_id)
        print(f"Notifying user {next_user_id} that audiobook '{audiobook.title}' is now available.")

    else:
        audiobook.is_available = True
        db.commit()
        print(f"Audiobook '{audiobook.title}' is now available for all users.")

    return {"message": f"Audiobook '{audiobook.title}' returned successfully."}

