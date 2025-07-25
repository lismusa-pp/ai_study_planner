from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

# Import your agents
from agents import time_agent, goal_agent, progress_tracker

app = Flask(__name__)

DATA_DIR = "data"
MOOD_LOG_FILE = os.path.join(DATA_DIR, "mood_log.json")
STUDY_LOG_FILE = os.path.join(DATA_DIR, "study_log.json")

def save_log(filename, data):
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood_value = int(request.form["mood"])
        # Log mood
        mood_log = {"date": datetime.now().isoformat(), "mood": mood_value}
        save_log(MOOD_LOG_FILE, mood_log)
        return redirect(url_for("schedule", mood=mood_value))
    return render_template("index.html")

@app.route("/schedule/<int:mood>", methods=["GET", "POST"])
def schedule(mood):
    tasks = goal_agent.prioritize_tasks()
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    if request.method == "POST":
        completed_sessions = request.form.getlist("completed")
        for subject in completed_sessions:
            log = {
                "date": datetime.now().isoformat(),
                "subject": subject,
                "completed": True
            }
            save_log(STUDY_LOG_FILE, log)
        return redirect(url_for("dashboard"))

    return render_template("schedule.html", schedule=schedule)

@app.route("/dashboard")
def dashboard():
    try:
        with open(STUDY_LOG_FILE, "r") as f:
            logs = [json.loads(line) for line in f]
    except FileNotFoundError:
        logs = []
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
