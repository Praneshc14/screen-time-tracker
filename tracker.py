import time
import psutil
import json
import os
from datetime import datetime
from collections import defaultdict

try:
    import pygetwindow as gw
except ImportError:
    print("Please install pygetwindow using: pip install pygetwindow")
    exit()

LOG_FILE = "screen_time_log.json"


def get_active_window():
    """Returns the title of the currently active window."""
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "Unknown"
    except Exception:
        return "Unknown"


def load_log():
    """Loads log data from the JSON file and ensures missing keys are handled."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            try:
                log_data = json.load(file)
                return log_data
            except json.JSONDecodeError:
                return {}  # Return an empty dict if JSON is corrupted
    return {}


def save_log(log_data):
    """Saves log data to the JSON file."""
    with open(LOG_FILE, "w") as file:
        json.dump(log_data, file, indent=4)


def track_screen_time():
    log_data = load_log()
    current_day = datetime.now().strftime("%Y-%m-%d")

    # Ensure the current day's key exists
    if current_day not in log_data:
        log_data[current_day] = {}

    last_window = None
    last_time = time.time()

    try:
        while True:
            active_window = get_active_window()
            if active_window != last_window and last_window is not None:
                elapsed_time = int(time.time() - last_time)

                # Ensure the last window exists in the current day's log
                if last_window not in log_data[current_day]:
                    log_data[current_day][last_window] = 0

                log_data[current_day][last_window] += elapsed_time
                save_log(log_data)
                last_time = time.time()

            last_window = active_window
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Tracking stopped. Data saved.")
        save_log(log_data)


if __name__ == "__main__":
    print("Tracking screen time. Press Ctrl+C to stop.")
    track_screen_time()
