from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from src.database import Base

IST = timezone("Asia/Kolkata")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(IST))

    lends = relationship("Lending", back_populates="user")