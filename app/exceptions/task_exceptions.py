from fastapi import HTTPException


class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Task not found")


class InvalidTaskDataException(HTTPException):
    def __init__(self, message: str = "Invalid task data"):
        super().__init__(status_code=400, detail=message)
