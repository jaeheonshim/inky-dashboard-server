from flask import Flask
from calendar_module import get_all_events, get_date_strings
from todoist_module import get_todo_items
from datetime import datetime
from cbor2 import dumps
import calendar_settings

calendar_days = 2

app = Flask(__name__)

@app.route("/")
def endpoint():
    now = datetime.now(calendar_settings.timezone)

    ### HEADER
    header_payload = {
        "d": now.strftime("%d"), # day
        "w": now.strftime("%A"), # day of week
        "s": now.strftime("%B %Y") # subtitle (month, year)
    }

    ### CALENDAR
    events = get_all_events(now, calendar_days)

    event_payload = []
    for event in events:
        event_payload.append({
            "co": event.color,
            "sd": event.start_day,
            "st": event.start_time,
            "ed": event.end_day,
            "et": event.end_time,
            "txt": event.text
        })

    calendar_payload = {
        "dh": get_date_strings(now, calendar_days),
        "ev": event_payload
    }

    ### TODOLIST
    tasks = get_todo_items(now)

    tasks_payload = []
    for task in tasks:
        tasks_payload.append({
            "txt": task.text,
            "sub": task.subtext
        })

    payload = {
        "hd": header_payload,
        "cal": calendar_payload,
        "tsk": tasks_payload
    }

    return dumps(payload)

if __name__=='__main__': 
   app.run() 
