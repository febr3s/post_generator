# test_scheduler.py
from scheduler import generate_schedule, count_posting_days
from config import START_DATE, END_DATE, POSTING_DAYS
from datetime import datetime

print("=== Testing scheduler ===\n")

schedule = generate_schedule()
print(f"Start date: {START_DATE}")
print(f"End date: {END_DATE}")
print(f"Posting days: {POSTING_DAYS} (0=Mon,4=Fri,5=Sat)")
print(f"Total posting days: {count_posting_days()}")
print(f"Schedule length: {len(schedule)}")

if schedule:
    print(f"\nFirst 5 posting dates:")
    for i, dt in enumerate(schedule[:5], 1):
        print(f"{i}. {dt.strftime('%a, %Y-%m-%d %H:%M')}")

    print(f"\nLast 5 posting dates:")
    for dt in schedule[-5:]:
        print(f"   {dt.strftime('%a, %Y-%m-%d %H:%M')}")

    # Verify all are at 11:00
    times_ok = all(dt.hour == 11 and dt.minute == 0 for dt in schedule)
    print(f"\nAll at 11:00? {times_ok}")

    # Verify no weekends except Friday/Saturday
    for dt in schedule:
        if dt.weekday() not in POSTING_DAYS:
            print(f"ERROR: {dt} is not a posting day!")
else:
    print("No schedule generated.")

print("\nTest complete.")