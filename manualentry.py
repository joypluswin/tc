import tkinter as tk
from tkinter import messagebox
import requests
import json

API_URL = "http://localhost/tc/save.php"  # Change to your actual API URL

def submit_form():
    data = {key: entry.get() for key, entry in entries.items()}

    try:
        response = requests.post(API_URL, json=data)
        res = response.json()

        if res.get("status") == "success":
            messagebox.showinfo("Success", res.get("message"))
        else:
            messagebox.showerror("Error", res.get("message"))

    except Exception as e:
        messagebox.showerror("Error", f"Could not send data: {e}")

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Manual TC Entry")

# Maximize the window to fit the screen
root.state('zoomed')  # For Windows: Maximizes the window

# For MacOS, use the following line to maximize
# root.attributes('-zoomed', True)

# For Linux (X11), you can use:
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.geometry(f"{screen_width}x{screen_height}")

root.configure(bg="white")

# --- Title Label ---
title = tk.Label(root, text="Manual TC Entry Form", font=("Helvetica", 20, "bold"), bg="white", fg="#004080")
title.pack(pady=20)

# --- Form Fields ---
fields = {
    "serials": "Serials",
    "rollnum": "Roll No",
    "college_name": "College Name",
    "district": "District",
    "student_name": "Student Name",
    "parent_name": "Parent Name",
    "nationality": "Nationality",
    "religion": "Religion",
    "caste": "Caste",
    "gender": "Gender",
    "dob": "Date of Birth",
    "admission_date": "Admission Date",
    "batch": "Batch",
    "partI": "Part I",
    "partIII": "Part III",
    "medium": "Medium",
    "fees_due": "Fee Due",
    "medical": "Medical Report",
    "date_left": "Left Date",
    "conduct": "Conduct",
    "applied_date": "TC Applied Date",
    "issue_date": "TC Issued Date",
    "qualified": "Qualified Status",
    "programme_study": "Programme of Study",
    "duration": "Duration",
    "umis_no": "UMIS No"
}

entries = {}
form_frame = tk.Frame(root, bg="white")
form_frame.pack(pady=10, padx=20)

# Creating form fields dynamically
for idx, (field_key, label_text) in enumerate(fields.items()):
    row = tk.Frame(form_frame, bg="white")
    row.grid(row=idx // 3, column=idx % 3, padx=20, pady=10, sticky="w")

    label = tk.Label(row, text=label_text + ":", font=("Segoe UI", 12), bg="white", anchor="w")
    label.pack(anchor="w")

    entry = tk.Entry(row, width=30, font=("Segoe UI", 12))
    entry.pack()

    entries[field_key] = entry

# --- Submit Button ---
submit_btn = tk.Button(root, text="Submit", command=submit_form,
                       font=("Segoe UI", 14, "bold"),
                       bg="#28a745", fg="white",
                       activebackground="#1e7e34",
                       width=20, height=2, relief="flat", cursor="hand2")
submit_btn.pack(pady=30)

root.mainloop()
