from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from src.database import Base


IST = timezone('Asia/Kolkata')


class Audiobook(Base):
    __tablename__ = 'audiobook'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    duration = Column(Integer, nullable=True)
    cover_image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(tz=IST))