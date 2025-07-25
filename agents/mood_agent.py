import json
from datetime import datetime
import tkinter as tk

def analyze_mood():
    def save_mood():
        mood_value = int(mood_scale.get())
        log = {"date": datetime.now().isoformat(), "mood": mood_value}
        with open("data/mood_log.json", "a") as f:
            f.write(json.dumps(log) + "\n")
        root.destroy()
        nonlocal mood_result
        mood_result = mood_value

    mood_result = 3  # default

    root = tk.Tk()
    root.title("🧠 How do you feel today?")
    root.geometry("300x150")

    tk.Label(root, text="Rate your mood (1 = Tired, 5 = Energized):").pack(pady=10)
    mood_scale = tk.Scale(root, from_=1, to=5, orient="horizontal")
    mood_scale.set(3)
    mood_scale.pack()

    tk.Button(root, text="Submit", command=save_mood).pack(pady=10)
    root.mainloop()
    return mood_result
