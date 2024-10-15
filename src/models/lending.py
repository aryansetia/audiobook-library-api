from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from src.database import Base

IST = timezone('Asia/Kolkata')

class Lending(Base):
    __tablename__ = 'lending'

    id = Column(Integer, primary_key=True, index=True)
    audiobook_id = Column(Integer, ForeignKey('audiobooks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrowed_at = Column(DateTime, default=lambda: datetime.now(IST))
    due_date = Column(DateTime, nullable=False)
    is_returned = Column(Boolean, default=False)

    audiobook = relationship('Audiobook', back_populates='lending')
    user = relationship('User', back_populates='lending')


