from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from src.database import Base

IST = timezone("Asia/Kolkata")

class Audiobook(Base):
    __tablename__ = "audiobooks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    cover_image_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(IST))
    is_available = Column(Boolean, nullable=False, default=True)

    lending = relationship("Lending", back_populates="audiobook")
    request_queue = relationship("RequestQueue", back_populates="audiobook")