import tkinter as tk
from tkinter import ttk, messagebox
import re

def parse_time_to_minutes(time_str):
    try:
        parts = list(map(int, time_str.strip().split(':')))
        if len(parts) == 3:
            return parts[0] * 60 + parts[1] + parts[2] / 60
        elif len(parts) == 2:
            return parts[0] + parts[1] / 60
        else:
            return float(time_str)
    except:
        return 0.0

def parse_pace_to_seconds(pace_str):
    try:
        match = re.match(r"(\d+)'(\d+)(?:\"|\")?", pace_str.strip())
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            return minutes * 60 + seconds
        return float(pace_str)
    except:
        return 0.0

def calculate_xp_status(data):
    try:
        def get_float(key, default=0.0):
            try:
                return float(data.get(key, default))
            except:
                return default

        muscle_mass = get_float("muscle_mass")
        body_fat = get_float("body_fat")
        training_load = get_float("training_load")
        max_pace = parse_pace_to_seconds(data.get("max_pace", "0"))
        stride_length = get_float("stride_length")
        workout_duration = parse_time_to_minutes(data.get("workout_duration", "0"))
        evening_walk_duration = parse_time_to_minutes(data.get("evening_walk_duration", "0"))
        sleep_duration = get_float("sleep_duration")
        sleep_score = get_float("sleep_score")
        sleep_deep = get_float("sleep_deep")
        avg_hr = get_float("avg_hr")
        bp_sys = get_float("bp_sys")
        spo2 = get_float("spo2")
        pulse = get_float("pulse")
        visceral_fat = get_float("visceral_fat")

        aerobic_score_workout = get_float("aerobic_score")
        aerobic_score_walk = get_float("aerobic_score_walk")
        anaerobic_score_workout = get_float("anaerobic_score")
        anaerobic_score_walk = get_float("anaerobic_score_walk")
        workout_calories = get_float("workout_calories")
        walk_calories = get_float("walk_calories")

        total_calories = workout_calories + walk_calories
        if total_calories > 0:
            combined_aerobic_score = (
                aerobic_score_workout * workout_calories +
                aerobic_score_walk * walk_calories
            ) / total_calories

            combined_anaerobic_score = (
                anaerobic_score_workout * workout_calories +
                anaerobic_score_walk * walk_calories
            ) / total_calories
        else:
            combined_aerobic_score = 0
            combined_anaerobic_score = 0

        #physical = max(0, min(100, (muscle_mass * 1.2 - body_fat * 0.8 + training_load * 0.3 - 40)))
        physical = max(0, min(100, (muscle_mass * 1.2 - body_fat * 1.0 + training_load * 0.3 - 40)))
        #speed = max(0, min(100, (110 - max_pace * 0.2 + (stride_length - 70) * 0.4)))
        speed = max(0, min(100, (110 - max_pace * 0.25 + (stride_length - 70) * 0.3)))
        #stamina = max(0, min(100, ((workout_duration + evening_walk_duration) * 0.4 + sleep_duration * 3 + combined_aerobic_score * 5 - 50)))
        stamina = max(0, min(100, ((workout_duration + evening_walk_duration) * 0.6 + sleep_duration * 3 + combined_aerobic_score * 5 - 50)))
        #durability = max(0, min(100, (sleep_duration * 5 + sleep_score * 0.8 + sleep_deep * 0.3 + combined_anaerobic_score * 3 - 80)))
        durability = max(0, min(100, (sleep_duration * 5 + sleep_score * 0.8 + sleep_deep * 0.5 + combined_anaerobic_score * 3 - 80)))
        #agility = max(0, min(100, ((stride_length - 60) * 1 + (130 - avg_hr) * 0.3)))
        agility = max(0, min(100, ((stride_length - 60) * 1.5 + (130 - avg_hr) * 0.5)))
        #vital = max(0, min(100, 100 - abs(bp_sys - 120) * 0.8 - abs(spo2 - 98) * 1.5 - abs(pulse - 70) * 0.5 - visceral_fat * 2))
        vital = max(0, min(100, 100 - abs(bp_sys - 120) * 3.75 - abs(spo2 - 98) * 1.5 - abs(pulse - 70) * 2.5 - visceral_fat * 2))

        xp = {
            "Physical": round(physical),
            "Speed": round(speed),
            "Stamina": round(stamina),
            "Durability": round(durability),
            "Agility": round(agility),
            "Vital": round(vital)
        }

        avg = sum(xp.values()) / 6
        if avg >= 90:
            rank = "S"
        elif avg >= 75:
            rank = "A"
        elif avg >= 60:
            rank = "B"
        elif avg >= 45:
            rank = "C"
        elif avg >= 30:
            rank = "D"
        elif avg >= 15:
            rank = "E+"
        else:
            rank = "E"

        return rank, xp

    except Exception as e:
        raise ValueError("Error in XP calculation: " + str(e))

def submit():
    data = {key: entry.get() if not isinstance(entry, ttk.Combobox) else entry.get() for key, entry in entries.items()}
    try:
        rank, xp = calculate_xp_status(data)
        result_text = f"Rank: {rank}\n" + "\n".join([f"{k}: {v}/100" for k, v in xp.items()])
        for key in xp:
            bars[key].set(xp[key])
            labels[key]["text"] = f"{xp[key]}/100"
        messagebox.showinfo("XP Status", result_text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Health XP Status Evaluator")
root.geometry("700x600")

main_canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

fields = [
    ("Age", "age"),
    ("Gender", "gender"),
    ("BP Systolic", "bp_sys"), ("BP Diastolic", "bp_dia"), ("Pulse", "pulse"), ("SpO2", "spo2"),
    ("Sleep Duration (hrs)", "sleep_duration"), ("Sleep Score", "sleep_score"),
    ("Deep Sleep %", "sleep_deep"), ("Light Sleep %", "sleep_light"), ("REM Sleep %", "sleep_rem"),
    ("Avg Sleep HR", "avg_sleep_hr"), ("Avg Sleep SpO2", "avg_sleep_spo2"),
    ("Weight", "weight"), ("BMI", "bmi"), ("Body Fat %", "body_fat"),
    ("Muscle Mass", "muscle_mass"), ("Muscle %", "muscle_percent"), ("Body Water %", "body_water"),
    ("Protein %", "protein_percent"), ("Bone %", "bone_percent"), ("Skeletal Muscle Mass", "skeletal_muscle"),
    ("Visceral Fat Rating", "visceral_fat"), ("BMR", "bmr"), ("Waist-to-Hip Ratio", "waist_hip"),
    ("Workout Calories", "workout_calories"), ("Workout Duration (hh:mm:ss)", "workout_duration"),
    ("Evening Walk Duration (hh:mm:ss)", "evening_walk_duration"),
    ("Avg HR", "avg_hr"), ("Max HR", "max_hr"), ("Aerobic Score", "aerobic_score"),
    ("Aerobic Score (Evening Walk)", "aerobic_score_walk"), ("Walk Calories", "walk_calories"),
    ("Anaerobic Score", "anaerobic_score"), ("Anaerobic Score (Evening Walk)", "anaerobic_score_walk"),
    ("Training Load", "training_load"),
    ("Stride Length (cm)", "stride_length"), ("Max Pace (mm'ss\"), e.g. 6'24\"", "max_pace")
]

entries = {}
for i, (label, key) in enumerate(fields):
    ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, sticky=tk.W)
    if key == "gender":
        entry = ttk.Combobox(scrollable_frame, values=["Male", "Female"], state="readonly")
        entry.set("Male")
    else:
        entry = ttk.Entry(scrollable_frame)
    entry.grid(row=i, column=1)
    entries[key] = entry

submit_button = ttk.Button(scrollable_frame, text="Evaluate", command=submit)
submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

bars = {}
labels = {}
xp_keys = ["Physical", "Speed", "Stamina", "Durability", "Agility", "Vital"]
for i, key in enumerate(xp_keys):
    ttk.Label(scrollable_frame, text=key).grid(row=len(fields)+1+i, column=0, sticky=tk.W)
    bars[key] = tk.IntVar()
    progress = ttk.Progressbar(scrollable_frame, orient="horizontal", length=200, mode="determinate", maximum=100, variable=bars[key])
    progress.grid(row=len(fields)+1+i, column=1, sticky=tk.W)
    labels[key] = ttk.Label(scrollable_frame, text="0/100")
    labels[key].grid(row=len(fields)+1+i, column=2, sticky=tk.W)

root.mainloop()
