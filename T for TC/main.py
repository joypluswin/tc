import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import dashboard  # Your custom dashboard script

def login(event=None):
    user = user_entry.get()
    pwd = pass_entry.get()
    if user.startswith("admins") and pwd == "1234":
        shift = user[-1]  # Last character "1" or "2"
        root.destroy()
        dashboard.open_dashboard(shift)  # Pass to dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

def clear_entry(event, entry, default_text, is_password=False):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        if is_password:
            entry.config(show="*")
        else:
            entry.config(show="")

def restore_entry(event, entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.config(show="")

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Login Page")

# Maximize the window to fit the screen
root.state('zoomed')  # This will maximize the window (for Windows)

# For MacOS, use the following line to maximize
# root.attributes('-zoomed', True)

# For Linux (X11), you can use:
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.geometry(f"{screen_width}x{screen_height}")

root.configure(bg="white")

# --- Style Configuration ---
style = ttk.Style()
style.configure("TEntry", padding=10, relief="flat", font=("Segoe UI", 14))
style.configure("TButton", padding=10, font=("Segoe UI", 14, "bold"), background="#3498db", foreground="white")
style.map("TButton",
          background=[("active", "#2e86de")],
          foreground=[("active", "white")])

# --- Logo ---
logo_path = os.path.join("assets", "sjc_logo_Final.png")
logo_img = Image.open(logo_path).resize((140, 250))
logo = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(root, image=logo, bg="white")
logo_label.image = logo
logo_label.pack(pady=20)

# --- Frame for form ---
form_frame = tk.Frame(root, bg="white")
form_frame.pack(pady=10)

# Shift Label
shift_label = tk.Label(form_frame, text="TC ENTRY PORTAL (SHIFT 1)", font=("Segoe UI", 16, "bold"), bg="white", fg="#5334CB")
shift_label.pack(pady=5)

# --- User ID Entry ---
user_entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 14))
user_entry.insert(0, "User ID")
user_entry.bind("<FocusIn>", lambda e: clear_entry(e, user_entry, "User ID"))
user_entry.bind("<FocusOut>", lambda e: restore_entry(e, user_entry, "User ID"))
user_entry.pack(pady=10, ipady=8)

# --- Password Entry ---
pass_entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 14))
pass_entry.insert(0, "Password")
pass_entry.bind("<FocusIn>", lambda e: clear_entry(e, pass_entry, "Password", is_password=True))
pass_entry.bind("<FocusOut>", lambda e: restore_entry(e, pass_entry, "Password"))
pass_entry.pack(pady=15, ipady=8)

# --- Custom Login Button (Button instead of TTK for full color control) ---
def on_enter(e):
    login_btn.config(bg="#2e86de")

def on_leave(e):
    login_btn.config(bg="#3498db")

login_btn = tk.Button(form_frame, text="Login", command=login, font=("Segoe UI", 14, "bold"),
                      bg="#3498db", fg="white", activebackground="#2e86de", relief="flat", width=15, height=1)
login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)
login_btn.pack(pady=15)

# --- Footer Note ---
footer = tk.Label(root, text="© St. Joseph's College", font=("Segoe UI", 10), bg="white", fg="gray")
footer.pack(side="bottom", pady=10)

# --- Bind Enter and Tab keys to trigger the login ---
user_entry.bind("<Return>", lambda event: pass_entry.focus())  
# Press Tab to go to password field
pass_entry.bind("<Return>", login)
# Press Enter to login
root.mainloop()
