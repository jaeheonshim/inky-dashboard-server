This is the backend server repository for my E-paper dashboard project, [Inky Dashboard](https://github.com/jaeheonshim/inky-dashboard). It's a simple Flask webserver that makes various HTTP requests to the provided iCal links as well as the the Todoist API, and encodes the most recent information in the [cbor](https://cbor.io/) format to be read by the Pico W powering the Inky Frame.

## How to use

Create a file named `calendar_settings.py` in the src directory. Below is a template for you to use when specifying settings in the file.

```py
from zoneinfo import ZoneInfo

# In ([ICS_URL], [color]) format where [color] is an int corresponding to one of the 7 inky frame colors
# BLACK     0
# WHITE     1
# GREEN     2
# BLUE      3
# RED       4
# YELLOW    5
# ORANGE    6

calendars = [
    ("https://example.com/example_calendar.ics", 6),
]

# Your current timezone
timezone = ZoneInfo("America/New_York")

# Todoist API key
todoist_api_key = "[insert Todoist API key here]"
```