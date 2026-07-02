from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="Todo API", version="1.0.0")

# In-memory storage — resets whenever the pod restarts.
# (This is intentional for now — great way to *see* Kubernetes pod lifecycle in action.
# We'll swap this for Postgres later.)
todos: dict[str, dict] = {}


class TodoCreate(BaseModel):
    title: str
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoCreate):
    id: str


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/health")
def health():
    """Used by Kubernetes liveness/readiness probes."""
    return {"status": "ok"}


@app.get("/todos", response_model=list[Todo])
def list_todos():
    return list(todos.values())


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    todo_id = str(uuid4())
    new_todo = {"id": todo_id, **todo.model_dump()}
    todos[todo_id] = new_todo
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, update: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    stored = todos[todo_id]
    update_data = update.model_dump(exclude_unset=True)
    stored.update(update_data)
    todos[todo_id] = stored
    return stored


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]