from agents import time_agent, goal_agent, mood_agent, progress_tracker
from dashboard import display_schedule
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

def run_daily_schedule():
    print("🧠 AI Study Planner Running...\n")

    # Step 1: Get mood from GUI
    mood = mood_agent.analyze_mood()

    # Step 2: Get and prioritize tasks
    tasks = goal_agent.prioritize_tasks()

    # Step 3: Adjust tasks based on past performance
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)

    # ✅ Step 4: Create the schedule — make sure this line exists!
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    # Step 5: Display it
    display_schedule(schedule)

    # Step 6: Ask user for completion input
    for block in schedule:
        log_completion(block["subject"])
