# Задание №3
# Создать API для управления списком задач.
# Каждая задача должна содержать поля "название",
# "описание" и "статус" (выполнена/не выполнена).
# API должен позволять выполнять CRUD операции с задачами.

from typing import List
from .pydantic_models import TaskIn, TaskOut
import databases
import sqlalchemy
from fastapi import FastAPI

DATABASE_URL = "sqlite:///homework6_task1.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("status", sqlalchemy.Boolean()),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={
                                  "check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


@app.post("/tasks/", response_model=TaskOut)
async def create_task(task: TaskIn): 
    query = tasks.insert().values(title=task.title,
                                  description=task.description)
    last_record_id = await database.execute(query)
    return {**task.model_dump(), "id": last_record_id}


@app.get("/tasks/", response_model=List[TaskOut])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/tasks/{task_id}", response_model=TaskOut)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, new_task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.model_dump())
    await database.execute(query)
    return {**new_task.model_dump(), "id": task_id}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task deleted'}