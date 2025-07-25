import json
from datetime import datetime

def prioritize_tasks():
    with open("data/tasks.json", "r") as f:
        tasks = json.load(f)

    # Convert deadlines to datetime for sorting
    for task in tasks:
        task["deadline_dt"] = datetime.strptime(task["deadline"], "%Y-%m-%d")

    # Sort by deadline ascending, then importance descending
    sorted_tasks = sorted(tasks, key=lambda t: (t["deadline_dt"], -t["importance"]))

    # Remove temporary datetime before returning
    for task in sorted_tasks:
        del task["deadline_dt"]

    return sorted_tasks
