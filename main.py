from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []
task_id = 1

class NewTask(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=200)

class TaskUpdate(BaseModel):
    done: bool

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool

@app.post("/tasks", status_code=201, response_model=TaskOut, summary="Создать новую задачу")
def create_task(task: NewTask):
    global task_id
    new_item = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "done": False
    }
    tasks.append(new_item)
    task_id += 1
    return new_item

@app.get("/tasks", response_model=list[TaskOut], summary="Получить список всех задач")
def get_tasks(done: bool | None = None):
    if done is not None:
        filtered = []
        for task in tasks:
            if task["done"] == done:
                filtered.append(task)
        return filtered
    else:
        return tasks

@app.get("/tasks/{task_id}", response_model=TaskOut, summary="Получить одну задачу")
def get_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")
  
@app.delete("/tasks/{task_id}", status_code=204, summary="Удалить задачу")
def delete_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Такой задачи для удаления нет")

@app.patch("/tasks/{task_id}", summary="Обновить статус задачи")
def change_status_done(task_id: int, task_status: TaskUpdate):
    for task in tasks:
        if task_id == task["id"]:
            task["done"] = task_status.done
            return {"status": "Статус изменен"}
    raise HTTPException(status_code=404, detail="Задача не найдена")

