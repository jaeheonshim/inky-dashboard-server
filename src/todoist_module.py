import calendar_settings
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from datetime import datetime, timezone

api = TodoistAPI(calendar_settings.todoist_api_key)

class TodoItem:
    def __init__(self, text, subtext):
        self.text = text
        self.subtext = subtext

def get_subtext(current: datetime, task: Task):
    if task.due.datetime:
        dt = datetime.strptime(task.due.datetime, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        month_day = dt.strftime("%b %d %I:%M %p")
    else:
        dt = datetime.strptime(task.due.date, "%Y-%m-%d")
        month_day = dt.strftime("%b %d")

    dt = dt.astimezone(current.tzinfo) # Use current timezone

    day_of_week = dt.strftime("%A")

    if current > dt:
        return f"{month_day} · Overdue"
    elif (dt - current).days == 1:
        return f"{month_day} · {day_of_week} · Today"
    elif (dt - current).days == 2:
        return f"{month_day} · {day_of_week} · Tomorrow"
    else:
        return f"{month_day} · {day_of_week}"

def get_todo_items(current: datetime, limit: int = 7):
    tasks = api.get_tasks()
    
    items = []

    for task in tasks[:limit]:
        items.append(TodoItem(
            task.content,
            get_subtext(current, task)
        ))

    return items