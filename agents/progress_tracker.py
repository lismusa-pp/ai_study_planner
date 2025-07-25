import json
from datetime import datetime

def adjust_tasks(tasks):
    try:
        with open("data/study_log.json", "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
    except:
        logs = []

    completed = sum(1 for log in logs[-5:] if log["completed"])  # last 5 days
    recent_success = completed / max(1, len(logs[-5:]))

    if recent_success < 0.5:
        print("⚠️ You're falling behind. Fewer tasks suggested today.")
        return tasks[:len(tasks)//2]
    return tasks


