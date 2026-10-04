from pydantic import BaseModel
from datetime import date

class TaskRead(BaseModel):
    title: str
    description: str
    due_date: date | None = None
    is_done: bool

class TaskCreate(BaseModel):
    id: int
    title: str
    description: str
    due_date: date
    is_daily: bool
    is_done: bool