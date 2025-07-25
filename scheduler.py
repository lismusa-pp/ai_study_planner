from agents import time_agent, goal_agent, mood_agent, progress_tracker
from dashboard import display_schedule

def run_daily_schedule():
    print("🧠 AI Study Planner Running...\n")
    
    mood = mood_agent.analyze_mood()
    tasks = goal_agent.prioritize_tasks()
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    display_schedule(schedule)


from datetime import datetime
import json

def log_completion(subject):
    completed = input(f"✅ Did you complete '{subject}'? (y/n): ").lower().startswith("y")
    log = {
        "date": datetime.now().isoformat(),
        "subject": subject,
        "completed": completed
    }
    with open("data/study_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# Replace this in run_daily_schedule:
for block in schedule:
    log_completion(block["subject"])
