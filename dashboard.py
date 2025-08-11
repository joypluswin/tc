import tkinter as tk
import subprocess
import os
import sys

def open_dashboard(shift):
    # Set shift as environment variable for child processes
    os.environ["SHIFT"] = shift

    dash = tk.Tk()
    dash.title("Menu - Shift " + shift)
    
    # Maximize window to fill the screen
    dash.state('zoomed')  # For Windows: Maximizes the window
    # For MacOS, use the following line to maximize
    # dash.attributes('-zoomed', True)
    # For Linux (X11), you can use:
    # screen_width = dash.winfo_screenwidth()
    # screen_height = dash.winfo_screenheight()
    # dash.geometry(f"{screen_width}x{screen_height}")

    dash.configure(bg="#f5faff")  # Light blue background

    # Fonts
    header_font = ("Segoe UI", 26, "bold")
    button_font = ("Segoe UI", 14, "bold")

    # Header Label
    header_label = tk.Label(
        dash,
        text=f"Transfer Certificate (TC) Menu - Shift {shift}",
        font=header_font,
        bg="#f5faff",
        fg="#2c3e50"
    )
    header_label.pack(pady=50)

    # Styled Button Creation
    def create_button(text, command):
        btn = tk.Button(
            dash,
            text=text,
            command=command,
            font=button_font,
            bg="#007acc",
            fg="white",
            activebackground="#005999",
            activeforeground="white",
            relief="flat",
            height=2,
            width=25,
            bd=0,
            cursor="hand2"
        )

        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg="#005999"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#007acc"))
        btn.pack(pady=20)

    # Manual TC Entry button
    def open_manualentry():
        manual_path = os.path.join(os.getcwd(), "manualentry.py")
        subprocess.Popen([sys.executable, manual_path], env=os.environ.copy())

    # Generate TC button
    def open_newtc():
        newtc_path = os.path.join(os.getcwd(), "newtc.py")
        subprocess.Popen([sys.executable, newtc_path], env=os.environ.copy())

    # Add Buttons
    create_button("Manual TC Entry", open_manualentry)
    create_button("Generate TC", open_newtc)

    def logout():
        dash.destroy()  # Close the dashboard window
        # Re-run main.py
        login_path = os.path.join(os.getcwd(), "main.py")
        subprocess.Popen([sys.executable, login_path])

    # Add Logout Button at the bottom
    logout_btn = tk.Button(
        dash,
        text="Logout",
        command=logout,
        font=("Segoe UI", 12, "bold"),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        relief="flat",
        height=1,
        width=10,
        cursor="hand2"
    )
    logout_btn.pack(side="top", pady=20)

    # Footer
    footer_label = tk.Label(
        dash,
        text="© Created by JCICT-ERP Team",
        font=("Segoe UI", 10),
        bg="#f5faff",
        fg="gray"
    )
    footer_label.pack(side="bottom", pady=20)

    dash.mainloop()
