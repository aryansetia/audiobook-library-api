from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from src.database import Base

IST = timezone("Asia/Kolkata")

class RequestQueue(Base):
    __tablename__ = 'request_queue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    audiobook_id = Column(Integer, ForeignKey('audiobooks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)

    audiobook = relationship("Audiobook", back_populates="request_queue")
    user = relationship("User", back_populates="request_queue")