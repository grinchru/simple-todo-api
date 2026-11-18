from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []

class NewTask(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=200)

@app.post("/tasks", status_code=201)
def create_task(task: NewTask):
    new_item = {
        "id": len(tasks) + 1,
        "title": task.title,
        "description": task.description,
        "done": False
    }
    tasks.append(new_item)
    return new_item

@app.get("/tasks")
def get_tasks():
    return tasks
