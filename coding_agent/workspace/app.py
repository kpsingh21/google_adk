from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Todo API")

# In-memory list to store todos
todos: List[dict] = []


class TodoCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_todo(todo: TodoCreate):
    next_id = max([t["id"] for t in todos], default=0) + 1
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }
    todos.append(new_todo)
    return new_todo


@app.get("/todos", response_model=List[TodoResponse])
@app.get("/todos/", response_model=List[TodoResponse], include_in_schema=False)
def list_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.put("/todos/{todo_id}", response_model=TodoResponse)
@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    for todo in todos:
        if todo["id"] == todo_id:
            update_data = todo_update.model_dump(exclude_unset=True)
            todo.update(update_data)
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(i)
            return {"message": "Todo deleted successfully", "todo": deleted_todo}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
