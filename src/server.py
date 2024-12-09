from flask import Flask
from calendar_module import get_all_events, get_date_strings
from datetime import datetime

calendar_days = 2

app = Flask(__name__)

@app.route("/")
def hello_world():
    now = datetime.now()
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

    return calendar_payload