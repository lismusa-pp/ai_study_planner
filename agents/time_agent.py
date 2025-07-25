from datetime import datetime, timedelta

def create_schedule(tasks, mood):
    pomodoro = 25  # minutes
    break_time = 5

    total_blocks = 6 if mood >= 3 else 3  # more energy = more sessions
    now = datetime.now()
    schedule = []

    for i in range(min(total_blocks, len(tasks))):
        task = tasks[i]
        start = now
        end = now + timedelta(minutes=pomodoro)
        schedule.append({
            "subject": task["name"],
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M")
        })
        now = end + timedelta(minutes=break_time)

    return schedule
