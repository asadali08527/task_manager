import datetime

from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String

from ..database.db import Base


class Task(Base):
    """Model for Task entity."""

    __tablename__ = "routers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    deleted = Column(Boolean, default=False)  # New column for soft delete
    deleted_at = Column(DateTime, nullable=True)


Index("ix_tasks_completed", Task.completed)
