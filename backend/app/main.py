from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select

from app.schemas import TaskCreate, TaskRead
from app.database import create_db, get_session
from app.models import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(title="ToDoList", lifespan=lifespan)

def find_task(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def is_complete(task: Task, today: date) -> bool:
    if task.is_daily:
        return task.last_completed == today
    else:
        return task.is_done

def to_read(task: Task, today: date) -> TaskRead:
    return TaskRead(
        **task.model_dump(exclude={"is_done"}),
        is_done=is_complete(task, today),
    )


@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return to_read(task, date.today())

@app.get("/tasks", response_model=list[TaskRead])
def read_tasks(overdue: bool = False, session: Session = Depends(get_session)):
    today = date.today()
    query = select(Task)
    if overdue:
        query = query.where(Task.due_date < today)
    tasks = session.exec(query).all()
    result = [to_read(t, today) for t in tasks]
    if overdue:
        result = [t for t in result if not t.is_done]
    return result

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    return to_read(find_task(task_id, session), date.today())

@app.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: int, session: Session = Depends(get_session)):
    task = find_task(task_id, session)
    if not task.is_daily:
        task.is_done = True
    else:
        task.last_completed = date.today()
    session.add(task)
    session.commit()
    session.refresh(task)
    return to_read(task, date.today())

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = find_task(task_id, session)
    session.delete(task)
    session.commit()


