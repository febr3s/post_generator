# scheduler.py
from datetime import datetime, timedelta, time
from typing import List
from config import START_DATE, END_DATE, POSTING_DAYS, POSTING_HOUR, POSTING_MINUTE

def generate_schedule() -> List[datetime]:
    """
    Generate a list of all posting dates between START_DATE and END_DATE (inclusive)
    on the days specified in POSTING_DAYS (Monday=0, Friday=4, Saturday=5)
    at the time POSTING_HOUR:POSTING_MINUTE.
    """
    schedule = []
    current = START_DATE
    while current <= END_DATE:
        if current.weekday() in POSTING_DAYS:
            # Create datetime with the correct time
            posting_datetime = datetime.combine(current.date(), time(POSTING_HOUR, POSTING_MINUTE))
            schedule.append(posting_datetime)
        current += timedelta(days=1)
    return schedule

def get_posting_dates() -> List[datetime]:
    """Wrapper to generate schedule and return it."""
    return generate_schedule()

def count_posting_days() -> int:
    """Return the total number of posting days in the schedule."""
    return len(generate_schedule())