import os
import json
import logging
try:
    import pygetwindow as gw
except ImportError:
    print("Please install pygetwindow using: pip install pygetwindow")
    exit()

LOG_FILE = "screen_time_log.json"

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_active_window():
    """
    Gets the title of the active window every time this function is called.
    """
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "Unknown"
    except Exception as e:
        logging.error(f"Error getting active window: {e}")
        return "Unknown"

def load_log():
    """
    Loads the screen time log from the JSON file.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_log(log_data):
    """
    Saves the screen time log into a JSON file.
    """
    try:
        with open(LOG_FILE, "w") as file:
            json.dump(log_data, file, indent=4)
    except Exception as e:
        logging.error(f"Error saving log: {e}")
