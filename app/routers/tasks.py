from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database.db import SessionLocal
from ..exceptions.task_exceptions import InvalidTaskDataException
from ..schemas.tasks_schemas import (TaskDeleteResponse, TaskInput,
                                     TaskPartialUpdate, TaskResponse)
from ..services.task_service import TaskService

router = APIRouter()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(
    completed: Optional[bool] = Query(None), db: Session = Depends(get_db)
) -> List[TaskResponse]:
    """
    Retrieve a list of all tasks or filter by completion status.

    - **completed**: Optional boolean to filter tasks by their
                    completion status.
    - **Response**: A list of tasks.
    """
    tasks = TaskService.get_all_tasks(db, completed)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """
    Retrieve details of a specific task.

    - **task_id**: The unique identifier of the task.
    - **Response**: Details of the requested task.
    """
    task = TaskService.get_task_by_id(task_id, db)
    return TaskResponse.model_validate(task)


@router.post("/tasks", response_model=TaskResponse)
def add_task(task_data: TaskInput,
             db: Session = Depends(get_db)) -> TaskResponse:
    """
    Create a new task.

    - **task_data**: The task details (title, description,
                    and completion status).
    - **Response**: The created task with its unique ID and timestamps.
    """
    if not task_data.title or not task_data.title.strip():
        raise InvalidTaskDataException(
            "Title is required and cannot be empty.")
    task = TaskService.create_task(task_data.model_dump(exclude_unset=True), db)
    return TaskResponse.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def modify_task(
    task_id: int, task_data: TaskInput, db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update an existing task.

    - **task_id**: The unique identifier of the task to be updated.
    - **task_data**: The new task details to replace the existing task.
    - **Response**: The updated task.
    """
    if "title" in task_data and not task_data["title"].strip():
        raise InvalidTaskDataException("Title cannot be empty.")
    task = TaskService.update_task(
        task_id, task_data.model_dump(exclude_unset=True), db)
    return TaskResponse.model_validate(task)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def partially_modify_task(
    task_id: int, task_data: TaskPartialUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Partially update an existing task.

    - **task_id**: The unique identifier of the task to be updated.
    - **task_data**: The fields to update in the task.
    - **Response**: The updated task with the modified fields.
    """
    if not any(
            [task_data.title is not None,
             task_data.description is not None,
             task_data.completed is not None]
    ):
        raise InvalidTaskDataException(
            "At least one of 'title', 'description', "
            "or 'completed' must be provided."
        )
    task = TaskService.partially_update_task(
        task_id, task_data.model_dump(exclude_unset=True), db
    )
    return TaskResponse.model_validate(task)


@router.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.

    - **task_id**: The unique identifier of the task to be deleted.
    - **Response**: A success message upon successful deletion.
    """
    TaskService.delete_task(task_id, db)
    return TaskDeleteResponse(detail=f"Task:{task_id} deleted successfully")
