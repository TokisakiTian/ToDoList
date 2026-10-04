from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    due_date: date | None = None
    is_done: bool = False
    is_daily: bool = False
    last_completed: date | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
