from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("data/study_log.json", "r") as f:
            logs = [json.loads(line) for line in f]
    except:
        logs = []

    html = """
    <h1>📈 Study Progress Dashboard</h1>
    <table border="1">
        <tr><th>Date</th><th>Subject</th><th>Completed</th></tr>
        {% for log in logs %}
        <tr>
            <td>{{ log['date'] }}</td>
            <td>{{ log['subject'] }}</td>
            <td>{{ '✅' if log['completed'] else '❌' }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
