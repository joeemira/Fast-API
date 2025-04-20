from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func

class POST(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, index=True)
    published = Column(Boolean, server_default='True', default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())