from datetime import date,timedelta
from app.models import Task
from app.main import is_complete

TODAY = date(2026, 1, 15)
TOMORROW = TODAY + timedelta(days=1)
YESTERDAY = TODAY - timedelta(days=1)

def test_daily_resets_next_day():
    task = Task(title="x", is_daily=True, last_completed=TODAY)
    assert is_complete(task, TODAY) == True
    assert is_complete(task, TOMORROW) == False