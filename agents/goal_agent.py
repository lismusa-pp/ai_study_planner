import json
from datetime import datetime

def prioritize_tasks():
    with open("data/tasks.json", "r") as f:
        tasks = json.load(f)

    # Sort by urgency first, then importance
    sorted_tasks = sorted(tasks, key=lambda t: (t["deadline"], -t["importance"]))

    return sorted_tasks
