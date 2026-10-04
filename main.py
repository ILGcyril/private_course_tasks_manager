from uuid import uuid4

from pydantic import BaseModel
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str


tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []

@app.get("/tasks")
def get_tasks()  -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)

    return new_task


@app.patch("/tasks/{id}")
def update_task(id: str, payload: TaskUpdateSchema) -> TaskSchema:
    for task in tasks:
        if task.id == id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed

        return task
    

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_task(id: str) -> None:
    for task in tasks:
        if task.id == id:
            tasks.remove(task)


@app.get("/categories")
def get_categories() -> list[CategorySchema]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    new_caregory = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(new_caregory)

    return new_caregory


@app.patch("/categories/{id}")
def update_category(id: str, payload: CategoryUpdateSchema) -> CategorySchema:
    for category in categories:
        if category.id == id:
            category.name = payload.name

            return category
        

@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str) -> None:
    for category in categories:
        if category.id == id:
            categories.remove(category)