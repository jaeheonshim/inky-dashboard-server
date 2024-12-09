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
    ("https://example.com", 2)
]

# Your current timezone
timezone = ZoneInfo("America/New_York")