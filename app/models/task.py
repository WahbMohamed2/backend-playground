from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, default="medium")
    status = Column(String, default="todo")
    due_date = Column(DateTime, nullable=True)
    
    # Automatic timestamp from the database server
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This links the task to a specific user
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)