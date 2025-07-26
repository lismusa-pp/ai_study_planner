from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

# Import your AI agent modules
from agents import time_agent, goal_agent, mood_agent, progress_tracker

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

DATA_DIR = "data"
MOOD_LOG_FILE = os.path.join(DATA_DIR, "mood_log.json")
STUDY_LOG_FILE = os.path.join(DATA_DIR, "study_log.json")

# Utility function to save log
def save_log(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")

@app.route("/plain-schedule")  # Renamed to avoid conflict
def plain_schedule():
    return render_template("schedule.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood_value = int(request.form["mood"])
        mood_log = {
            "date": datetime.now().isoformat(),
            "mood": mood_value
        }
        save_log(MOOD_LOG_FILE, mood_log)
        return redirect(url_for("schedule", mood=mood_value))
    return render_template("index.html")

@app.route("/schedule/<int:mood>", methods=["GET", "POST"])
def schedule(mood):
    # Get prioritized tasks
    tasks = goal_agent.prioritize_tasks()

    # Adjust tasks based on progress
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)

    # Generate study schedule
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    if request.method == "POST":
        completed_sessions = set(request.form.getlist("completed"))
        for session in schedule:
            subject = session["subject"]
            log = {
                "date": datetime.now().isoformat(),
                "subject": subject,
                "completed": subject in completed_sessions
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
