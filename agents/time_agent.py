from datetime import datetime, timedelta

def create_schedule(tasks, mood):
    pomodoro_duration = 25  # minutes
    break_duration = 5      # minutes
    total_blocks = 6 if mood >= 3 else 3

    now = datetime.now()
    schedule = []

    for i in range(min(total_blocks, len(tasks))):
        task = tasks[i]
        start_time = now
        end_time = now + timedelta(minutes=pomodoro_duration)
        schedule.append({
            "subject": task["name"],
            "start": start_time.strftime("%H:%M"),
            "end": end_time.strftime("%H:%M")
        })
        now = end_time + timedelta(minutes=break_duration)

    return schedule
