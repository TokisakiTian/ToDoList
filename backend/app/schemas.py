from pydantic import BaseModel
from datetime import date

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    due_date: date | None = None
    is_daily: bool
    is_done: bool

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    is_daily: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    is_daily: bool | None = None