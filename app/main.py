from fastapi import FastAPI

from .database.db import init_db
from .routers import tasks

app = FastAPI()

init_db()

app.include_router(tasks.router, tags=["Tasks"])
