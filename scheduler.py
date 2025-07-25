from agents import time_agent, goal_agent, mood_agent, progress_tracker
from dashboard import display_schedule

def run_daily_schedule():
    print("🧠 AI Study Planner Running...\n")
    
    mood = mood_agent.analyze_mood()
    tasks = goal_agent.prioritize_tasks()
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    display_schedule(schedule)