from ics import Calendar, Event
import requests
from datetime import datetime, timedelta, timezone, time
from dateutil.rrule import rrulestr
from zoneinfo import ZoneInfo
import os
import calendar_settings

class CalendarEvent:
    def __init__(self, color, start_day, start_time, end_day, end_time, text):
        self.color = color
        self.start_day = start_day
        self.start_time = start_time
        self.end_day = end_day
        self.end_time = end_time
        self.text = text

def get_events_between(cal: Calendar, color: int, start_date: datetime, end_date: datetime, zone: ZoneInfo):
    '''Returns all events that occur between a specific start and end date as a list of CalendarEvent objects'''
    event_data = []

    def get_day_time(date: datetime):
        date = date.astimezone(zone)
        return ((date - start_date.astimezone(zone)).days, date.hour * 100 + date.minute)

    for event in cal.events:
        rrule_found = False

        for extra in event.extra:
            if extra.name == "RRULE":
                # if the event is recurring, add every occurrence that lands between the start and end date
                rrule = extra.value
                rule = rrulestr(rrule, dtstart=event.begin.datetime)
                for occurrence_start in rule.between(start_date, end_date):
                    occurrence_end = occurrence_start + (event.end.datetime - event.begin.datetime)
                    event_data.append((color, *get_day_time(occurrence_start), *get_day_time(occurrence_end), event.name))
                rrule_found = True
                break

        if not rrule_found and event.begin <= end_date and start_date <= event.end:
            event_data.append((color, *get_day_time(event.begin), *get_day_time(event.end), event.name))

    return list(map(lambda edata: CalendarEvent(*edata), event_data))

def get_events_within_days_of_date(cal: Calendar, color: int, start_date: datetime, days: int):
    zone = calendar_settings.timezone
    start_of_today = datetime.combine(start_date, time.min, tzinfo=zone)

    return get_events_between(cal, color, start_of_today, start_of_today + timedelta(days=days), zone)

def get_all_events(start_date: datetime, days: int = 2):
    all_events = []

    for cal_data in calendar_settings.calendars:
        cal = Calendar(requests.get(cal_data[0]).text)
        all_events.extend(get_events_within_days_of_date(cal, cal_data[1], start_date, days))

    return all_events

def get_date_strings(start_date: datetime, days: int = 2):
    zone = calendar_settings.timezone
    current = datetime.combine(start_date, time.min, tzinfo=zone)

    strings = []

    for _ in range(days):
        strings.append(current.strftime("%A, %b %-d"))
        current += timedelta(days=1)

    return strings