# Task Manager API

## Overview

The Task Manager API is a simple backend application for managing tasks in a to-do list. It provides endpoints to create, retrieve, update, partially update, and delete tasks.

## Features

- Create tasks
- Retrieve all tasks or filter by completion status
- Retrieve details of a specific task
- Update a task
- Partially update a task
- Delete a task

---

## Installation

### Prerequisites

1. Install Python 3.9 or later.
2. Install [Poetry](https://python-poetry.org/docs/#installation).

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/asadali08527/task_manager.git
   cd task_manager
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

4. Start the server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

---

## Running Tests

1. Run tests using `pytest`:
   ```bash
   poetry run pytest
   ```

2. Check test coverage:
   ```bash
   poetry run pytest --cov=app
   ```

---

## Endpoints

### 1. Create Task
- **URL:** `POST /tasks`
- **Request Body:**
  ```json
  {
      "title": "New Title",
      "description": "Test description"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "title": "New Title",
      "description": "Test description",
      "completed": false,
      "created_at": "2024-12-18T22:46:01.584517"
  }
  ```

### 2. Fetch All Tasks
- **URL:** `GET /tasks`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "New Title",
          "description": "Test description",
          "completed": false,
          "created_at": "2024-12-18T22:46:01.584517"
      }
  ]
  ```

### 3. Fetch Tasks by Completion Status
- **URL:** `GET /tasks?completed=false`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "New Title",
          "description": "Test description",
          "completed": false,
          "created_at": "2024-12-18T22:46:01.584517"
      }
  ]
  ```

### 4. Fetch Task by ID
- **URL:** `GET /tasks/{task_id}`
- **Example:** `GET /tasks/1`
- **Response:**
  ```json
  {
      "id": 1,
      "title": "New Title",
      "description": "Test description",
      "completed": false,
      "created_at": "2024-12-18T22:46:01.584517"
  }
  ```

### 5. Update Task
- **URL:** `PUT /tasks/{task_id}`
- **Request Body:**
  ```json
  {
      "title": "Updated Title",
      "description": "Updated description",
      "completed": true
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "title": "Updated Title",
      "description": "Updated description",
      "completed": true,
      "created_at": "2024-12-18T22:46:01.584517"
  }
  ```

### 6. Partially Update Task
- **URL:** `PATCH /tasks/{task_id}`
- **Request Body:**
  ```json
  {
      "description": "Partially updated description"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "title": "Updated Title",
      "description": "Partially updated description",
      "completed": true,
      "created_at": "2024-12-18T22:46:01.584517"
  }
  ```

### 7. Delete Task
- **URL:** `DELETE /tasks/{task_id}`
- **Example:** `DELETE /tasks/1`
- **Response:**
  ```json
  {
      "detail": "Task:1 deleted successfully"
  }
  ```

---

## Notes
- Ensure the database is configured correctly before running the application.
- All endpoints return appropriate status codes and error messages for invalid requests.

---

## Contributing
Feel free to submit issues or pull requests to enhance the project.