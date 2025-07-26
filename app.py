from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

# AI agents
from agents import time_agent, goal_agent, mood_agent, progress_tracker

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Log model
class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        mood_value = int(request.form["mood"])
        return redirect(url_for("schedule", mood=mood_value))
    return render_template("index.html")

@app.route("/schedule/<int:mood>", methods=["GET", "POST"])
@login_required
def schedule(mood):
    tasks = goal_agent.prioritize_tasks()
    adjusted_tasks = progress_tracker.adjust_tasks(tasks)
    schedule = time_agent.create_schedule(adjusted_tasks, mood)

    if request.method == "POST":
        completed_sessions = set(request.form.getlist("completed"))
        for session in schedule:
            log = StudyLog(
                user_id=current_user.id,
                date=datetime.now().isoformat(),
                subject=session["subject"],
                completed=session["subject"] in completed_sessions
            )
            db.session.add(log)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("schedule.html", schedule=schedule)

@app.route("/dashboard")
@login_required
def dashboard():
    logs = StudyLog.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", logs=logs)

# Initialize DB if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
