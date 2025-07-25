import json
from datetime import datetime

def analyze_mood():
    mood = input("😌 Enter your mood today (1–5): ")
    mood = max(1, min(5, int(mood)))

    # Save to log
    log = {"date": datetime.now().isoformat(), "mood": mood}
    with open("data/mood_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

    return mood  # 1 = tired, 5 = energized


