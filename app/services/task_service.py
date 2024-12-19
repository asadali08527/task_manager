import datetime
import logging
from typing import Optional

from sqlalchemy.orm import Session

from ..exceptions.task_exceptions import (InvalidTaskDataException,
                                          TaskNotFoundException)
from ..models.task_model import Task

logger = logging.getLogger(__name__)


class TaskService:
    """
    Service class to handle all task-related business logic.
    Provides methods to create, retrieve, update, partially
    update, and delete tasks.
    """

    @staticmethod
    def get_all_tasks(db: Session, completed: Optional[bool] = None):
        """
        Retrieve all tasks or filter by their completion status.

        Args:
            db (Session): The database session.
            completed (Optional[bool]): Filter tasks by completion
                                        status (True/False).

        Returns:
            List[Task]: A list of tasks matching the filter criteria.

        Raises:
            InvalidTaskDataException: If an unexpected error occurs
                                    while querying tasks.
        """
        try:
            query = db.query(Task).filter(Task.deleted == False)
            if completed is not None:
                query = query.filter(Task.completed == completed)
            tasks = query.all()
            return tasks
        except Exception as e:
            logger.error(f"Error while retrieving tasks, error: {str(e)}")
            raise InvalidTaskDataException(f"Error retrieving tasks: {str(e)}")

    @staticmethod
    def get_task_by_id(task_id: int, db: Session):
        """
        Retrieve a specific task by its ID.

        Args:
            task_id (int): The unique identifier of the task.
            db (Session): The database session.

        Returns:
            Task: The task object with the given ID.

        Raises:
            TaskNotFoundException: If the task with the specified
                                    ID does not exist.
        """
        task = db.query(Task).filter(Task.id == task_id,
                                     Task.deleted == False).first()
        if not task:
            logger.error(f"Task:{task_id} not found")
            raise TaskNotFoundException()
        return task

    @staticmethod
    def create_task(task_data: dict, db: Session):
        """
        Create a new task in the database.

        Args:
            task_data (TaskInput): The input data for the task.
            db (Session): The database session.

        Returns:
            Task: The created task object.

        Raises:
            InvalidTaskDataException: If an unexpected error occurs
                                        while creating the task.
        """
        try:
            task = Task(**task_data)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise InvalidTaskDataException(f"Error creating task: {str(e)}")

    @staticmethod
    def update_task(task_id: int, task_data: dict, db: Session):
        """
        Update an existing task.

        Args:
            task_id (int): The unique identifier of the task to update.
            task_data (TaskInput): The new data to update the task.
            db (Session): The database session.

        Returns:
            Task: The updated task object.

        Raises:
            InvalidTaskDataException: If an unexpected error occurs
                                        while updating the task.
        """
        task = TaskService.get_task_by_id(task_id, db)
        try:
            for key, value in task_data.items():
                setattr(task, key, value)
            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            logger.error(
                f"Error while updating task:{task_id}, error: {str(e)}")
            raise InvalidTaskDataException(f"Error updating task: {str(e)}")

    @staticmethod
    def partially_update_task(task_id: int, task_data: dict, db: Session):
        """
        Partially update an existing task.

        Args:
            task_id (int): The unique identifier of the task to
                            partially update.
            task_data (TaskPartialUpdate): The partial data to
                                            update the task.
            db (Session): The database session.

        Returns:
            Task: The updated task object with modified fields.

        Raises:
            InvalidTaskDataException: If an unexpected error occurs while
                                        partially updating the task.
        """
        task = TaskService.get_task_by_id(task_id, db)
        try:
            for key, value in task_data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            logger.error(
                f"Error while partially updating task:{task_id}, "
                f"error: {str(e)}"
            )
            raise InvalidTaskDataException(
                f"Error partially updating task: {str(e)}")

    @staticmethod
    def delete_task(task_id: int, db: Session):
        """
        Delete a task by its ID.

        Args:
            task_id (int): The unique identifier of the task to delete.
            db (Session): The database session.

        Returns:
            dict: A success message upon successful deletion.

        Raises:
            InvalidTaskDataException: If an unexpected error occurs
                                        while deleting the task.
        """
        task = TaskService.get_task_by_id(task_id, db)
        try:
            task.deleted = True
            task.deleted_at = datetime.datetime.now()
            db.delete(task)
            db.commit()
        except Exception as e:
            logger.error(
                f"Error while deleting task:{task_id}, error: {str(e)}")
            raise InvalidTaskDataException(f"Error deleting task: {str(e)}")
