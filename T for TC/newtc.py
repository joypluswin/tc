import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import subprocess
import sys
import json

# ---------- Globals ----------
departments_list = []
API_BASE = "https://service.sjctni.edu/TC"
selected_vars = []

# ---------- Load Departments from Remote ----------
def load_departments():
    SHIFT = os.environ.get("SHIFT", "1")
    try:
        url = f"{API_BASE}/getdepartments_{SHIFT}.php"
        response = requests.get(url)
        if not response.content.strip():
            raise Exception("Empty response")
        departments = response.json()
        departments_list.clear()
        departments_list.extend(departments)
        dept_combobox['values'] = [f"{d['deptcode']} - {d['deptname']}" for d in departments]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load departments:\n{e}")

# ---------- Fetch Students from Remote URL ----------
def fetch_students():
    global selected_vars
    batch = batch_combobox.get()
    cls = class_combobox.get()
    dept = dept_combobox.get()
    SHIFT = os.environ.get("SHIFT", "1")

    if not all([batch, cls, dept]):
        messagebox.showwarning("Missing Fields", "Please fill all filters.")
        return

    # Process inputs
    batch_code = batch[-2:]  # e.g. 2025 -> 25
    class_code = cls[0].lower()  # UG -> u, PG -> p
    deptcode = dept.split(" - ")[0]  # e.g. CS

    try:
        url = f"{API_BASE}/regno.php"
        params = {
            "batch": batch_code,
            "class": class_code,
            "deptcode": deptcode,
            "shift": SHIFT
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        regnos = response.json()

        # Clear previous
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        selected_vars = []

        if not regnos:
            tk.Label(scrollable_frame, text="No matching students found.").pack()
            return
        # Wrap students into multiple columns
        max_rows = 40
        col = 0
        row = 0
        for reg in regnos:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(scrollable_frame, text=reg, variable=var, font=("Courier New", 12), anchor="w", padx=10)
            cb.grid(row=row, column=col, sticky="w")
            selected_vars.append((var, reg))
            row += 1
            if row >= max_rows:
                row = 0
                col += 1

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch students:\n{e}")

# ---------- Select All ----------
def select_all():
    for var, _ in selected_vars:
        var.set(True)

# ---------- Proceed to Next ----------
def go_to_next():
    selected_regnos = [reg for var, reg in selected_vars if var.get()]
    if not selected_regnos:
        messagebox.showwarning("No Selection", "Please select at least one student.")
        return

    shift = os.environ.get("SHIFT", "1")
    batch = batch_combobox.get()
    cls = class_combobox.get()
    dept = dept_combobox.get()

    if not all([batch, cls, dept]):
        messagebox.showwarning("Missing Fields", "Please fill all filters.")
        return

    batch_code = batch[-2:]              # e.g. 2025 -> "25"
    class_code = cls[0].lower()          # UG -> "u", PG -> "p"
    deptcode = dept.split(" - ")[0]      # e.g. "CS"

    data = {
        "shift": shift,
        "batch": batch_code,
        "class": class_code,
        "deptcode": deptcode,
        "selected_regnos": selected_regnos
    }

    try:
        with open("selected_data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save selected data:\n{e}")
        return

    try:
        subprocess.run([sys.executable, "print.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch print.py:\n{e}")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("TC Form - Student Selection")

# Maximize the window to fit the screen
root.state('zoomed')  # This will maximize the window (for Windows)

# For MacOS, use the following line to maximize
# root.attributes('-zoomed', True)

# For Linux (X11), you can use:
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.geometry(f"{screen_width}x{screen_height}")

root.configure(bg="#f8f8ff")

# ---------- Style Configuration ----------
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TCombobox", font=("Segoe UI", 12))

# ---------- Top Frame for Filters ----------
filters_frame = ttk.LabelFrame(root, text="Filter Students", padding=20)
filters_frame.pack(fill="x", padx=20, pady=10)

# Batch
ttk.Label(filters_frame, text="Batch:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
batch_combobox = ttk.Combobox(filters_frame, values=["2022","2023","2024","2025","2026","2027"], width=10)
batch_combobox.grid(row=0, column=1, padx=10, pady=5)

# UG/PG
ttk.Label(filters_frame, text="UG/PG:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
class_combobox = ttk.Combobox(filters_frame, values=["UG","PG"], width=10)
class_combobox.grid(row=0, column=3, padx=10, pady=5)

# Department
ttk.Label(filters_frame, text="Department:").grid(row=0, column=4, padx=10, pady=5, sticky="e")
dept_combobox = ttk.Combobox(filters_frame, width=30)
dept_combobox.grid(row=0, column=5, padx=10, pady=5)

# ---------- Main Frame with Canvas for Scrollable Students ----------
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

listbox_frame = ttk.LabelFrame(main_frame, text="Students", padding=10)
listbox_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

canvas = tk.Canvas(listbox_frame, width=1100, height=800)
scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)

# Enable Mouse Scroll on Canvas
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# ---------- Button Panel ----------
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=0, column=1, sticky="n", padx=20)

fetch_btn = ttk.Button(button_frame, text="Fetch Students", command=fetch_students)
fetch_btn.pack(pady=10, fill="x")

select_btn = ttk.Button(button_frame, text="Select All", command=select_all)
select_btn.pack(pady=10, fill="x")

next_btn = ttk.Button(button_frame, text="Next →", command=go_to_next)
next_btn.pack(pady=30, fill="x")

# ---------- Load Departments on Startup ----------
root.after(100, load_departments)

root.mainloop()
