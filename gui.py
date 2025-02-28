import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv
from datetime import datetime

LOG_FILE = "screen_time_log.json"


# Load screen time logs
def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    return {}


# Refresh logs in the GUI
def refresh_logs():
    logs = load_logs()
    tree.delete(*tree.get_children())  # Clear existing entries

    if not logs:
        tree.insert("", "end", values=("No logs available", "", ""))
        return

    for date, data in sorted(logs.items(), reverse=True):
        for window, time_spent in data.items():
            formatted_time = f"{time_spent // 60}m {time_spent % 60}s"
            tree.insert("", "end", values=(date, window, formatted_time))


# Export logs to CSV
def export_logs_to_csv():
    logs = load_logs()
    if not logs:
        messagebox.showwarning("Export Failed", "No logs available to export.")
        return

    filename = f"screen_time_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Window", "Time Spent (minutes:seconds)"])

        for date, data in logs.items():
            for window, time_spent in data.items():
                formatted_time = f"{time_spent // 60}m {time_spent % 60}s"
                writer.writerow([date, window, formatted_time])

    messagebox.showinfo("Export Successful", f"Logs exported to {filename}")


# Create the main GUI window
app = tk.Tk()
app.title("Screen Time Tracker")
app.geometry("900x600")
app.configure(bg="#121212")  # Dark theme background
app.state("zoomed")  # Start maximized


# Adjust layout when resized
def on_resize(event):
    tree_frame.place(relwidth=0.95, relheight=0.75, relx=0.025)
    button_frame.place(relwidth=0.95, rely=0.85, relx=0.025)


app.bind("<Configure>", on_resize)

# Title Label
title_label = tk.Label(app, text="Screen Time Tracker", font=("Arial", 20, "bold"), fg="white", bg="#121212")
title_label.pack(pady=15)

# Create table frame
tree_frame = tk.Frame(app, bg="#1E1E1E", bd=2, relief="ridge")
tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Create treeview (Table)
columns = ("Date", "Window", "Time Spent")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview")
tree.heading("Date", text="Date")
tree.heading("Window", text="Application / Window")
tree.heading("Time Spent", text="Time Spent")
tree.pack(fill="both", expand=True, padx=5, pady=5)

# Add scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Style customization
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.Treeview", background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E", rowheight=30)
style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"), background="#292929", foreground="white")
style.map("Custom.Treeview", background=[("selected", "#575757")])

# Buttons
button_frame = tk.Frame(app, bg="#121212")
button_frame.pack(fill="x")


def create_button(parent, text, command, color):
    return tk.Button(parent, text=text, command=command, font=("Arial", 12, "bold"), bg=color, fg="white", padx=15,
                     pady=8, bd=0, relief="ridge", activebackground="#333333")


refresh_button = create_button(button_frame, "Refresh Logs", refresh_logs, "#27AE60")
refresh_button.pack(side="left", padx=20, pady=10)

export_button = create_button(button_frame, "Export to CSV", export_logs_to_csv, "#E74C3C")
export_button.pack(side="right", padx=20, pady=10)

# Load logs initially
refresh_logs()

# Run the GUI app.mainloop()
app.mainloop()