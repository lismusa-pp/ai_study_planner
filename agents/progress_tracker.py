import json
from datetime import datetime

def adjust_tasks(tasks):
    try:
        with open("data/study_log.json", "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        logs = []

    completed_count = sum(1 for log in logs[-5:] if log.get("completed"))
    recent_success = completed_count / max(1, len(logs[-5:]))

    if recent_success < 0.5:
        print("⚠️ Falling behind, reducing today's tasks.")
        return tasks[:len(tasks)//2]
    return tasks
