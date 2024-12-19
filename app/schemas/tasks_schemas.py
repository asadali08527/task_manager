from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskInput(BaseModel):
    """Schema for validating task input data."""

    title: str = Field(
        ..., min_length=1, max_length=255, description="Title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description of the task"
    )
    completed: Optional[bool] = Field(
        False, description="Status of task completion")


class TaskPartialUpdate(BaseModel):
    """Schema for partially updating a task."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description of the task"
    )
    completed: Optional[bool] = Field(
        None, description="Status of task completion")


class TaskResponse(BaseModel):
    """
    Schema for a complete task response, including the ID and timestamps.
    """

    id: int
    title: str = Field(
        ..., min_length=1, max_length=255, description="Title of the task"
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Optional description of the task"
    )  # Explicitly set default=None
    completed: bool = Field(False, description="Status of task completion")
    created_at: datetime = Field(..., description="Timestamp when the task was created")
    deleted: bool = Field(False, description="Task deletion status")
    deleted_at: Optional[datetime] = Field(..., description="Timestamp when the task was deleted")

    class Config:
        # Define fields...
        from_attributes = True


class TaskDeleteResponse(BaseModel):
    """
    Schema for a successful task deletion response.
    """

    detail: str = Field(..., description="Details about the deletion status")
