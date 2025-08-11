import tkinter as tk
from tkinter import messagebox
import json
import requests
import urllib.parse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register the custom font
pdfmetrics.registerFont(TTFont("lucon-bold", "lucon.ttf"))

PAGE_WIDTH, PAGE_HEIGHT = A4

def cm(val):
    return val * 28.35

def fake_bold(c, text, x, y, layers, offset=0.3):
    for i in range(layers):
        c.drawString(x + i * offset, y, str(text))

def draw_tc_page(c, data):
    default_font = "lucon-bold"
    default_font_size = 12

    special_font_sizes = {
        "Numwords": 8,
        "student_name": 13.5
    }

    positions = {
        "serials": (3.4, 5.2),
        "rollnum": (15.2, 5.2),
        "student_name": (10.1, 7.46),
        "parent_name": (10.1, 8.46),
        "nationality": (10.1, 9.05),
        "religion": (10.1, 9.6),
        "caste": (10.1, 10.22),
        "gender": (10.1, 10.79),
        "dob": (10.1, 11.37),
        "Numwords": (10.1, 11.65),
        "admission_date": (10.1, 12.45),
        "batch": (10.1, 13.3),
        "partI": (10.1, 14.3),
        "partIII": (10.1, 14.9),
        "medium": (10.1, 15.4),
        "fees_due": (10.1, 16.15),
        "medical": (10.1, 17.23),
        "date_left": (10.1, 18.7),
        "conduct": (10.1, 19.72),
        "applied_date": (10.1, 20.39),
        "issue_date": (10.1, 21.55),
        "qualified": (10.1, 22.25),
        "programme_study": (10.1, 23.23),
        "duration": (10.1, 23.93),
        "umis_no": (10.1, 24.65)
    }

    for key, (x_cm, y_cm) in positions.items():
        font_size = special_font_sizes.get(key, default_font_size)
        text = str(data.get(key, "--------") or "--------")
        x = cm(x_cm)
        y = PAGE_HEIGHT - cm(y_cm)
        c.setFont(default_font, font_size)

        if key == "student_name":
            fake_bold(c, text, x, y, layers=3, offset=0.3)
        else:
            fake_bold(c, text, x, y, layers=2, offset=0.3)

def generate():
    try:
        with open("selected_data.json") as f:
            config = json.load(f)
    except Exception:
        messagebox.showerror("Error", "Missing or unreadable selection data file.")
        return

    batch = config.get("batch")       # already last two digits
    shift = config.get("shift")
    student_class = config.get("class")
    deptcode = config.get("deptcode")
    regnos = config.get("selected_regnos", [])

    if not regnos:
        messagebox.showwarning("Empty", "No students selected.")
        return

    regnos_quoted = urllib.parse.quote(",".join([f"'{r}'" for r in regnos]))

    url = (
        f"https://service.sjctni.edu/TC/getdata.php?"
        f"batch={batch}&class={student_class}&deptcode={deptcode}&shift={shift}&regN={regnos_quoted}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, str):
            raise ValueError("Server returned a string instead of JSON list.")

        if not isinstance(data, list) or not data:
            raise ValueError("No student data returned or unexpected format.")

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch data from server.\n{str(e)}")
        return

    c = canvas.Canvas("tc_output.pdf", pagesize=A4)
    serial_no = 1000
    for student in data:
        student_data = {
            "serials": str(serial_no),
            "rollnum": student.get("regNo", "--------"),
            "student_name": student.get("STUD_uGXX_NAME", "--------"),
            "parent_name": student.get("stud_ugxx_fname", "--------"),
            "nationality": student.get("STUD_uGXX_NATIONALITY", "--------"),
            "religion": student.get("STUD_uGXX_RELIGION", "--------"),
            "caste": student.get("stud_ugxx_castename", "--------"),
             "gender": (
                "MALE" if str(student.get("STUD_uGXX_SEX", "")).strip() == "1"
                        else "FEMALE" if str(student.get("STUD_uGXX_SEX", "")).strip() == "2"
                        else "OTHERS"
                ),
            "dob": student.get("STUD_uGXX_DOB", "--------"),
            "admission_date": student.get("stud_ugxx_admit", "--------"),
            "batch": student.get("batch", "--------"),
            "partI": student.get("partI", "--------"),
            "partIII": student.get("partIII", "--------"),
            "medium": student.get("medium", "English"),
            "fees_due": student.get("fees_due", "--------"),
            "medical": student.get("medical", "--------"),
            "date_left": student.get("stud_ugxx_leftdate", "--------"),
            "conduct": student.get("conduct", "--------"),
            "applied_date": student.get("stud_ugxx_applydate", "--------"),
            "issue_date": student.get("issue_date", "--------"),
            "qualified": student.get("qualified", "--------"),
            "programme_study": student.get("programme_study", "--------"),
            "duration": student.get("stud_ugxx_acadamicyear", "--------"),
            "umis_no": student.get("stud_ugxx_umis", "--------"),
        }
        draw_tc_page(c, student_data)
        c.showPage()
        serial_no += 1

    c.save()
    messagebox.showinfo("Success", "PDF generated successfully as 'tc_output.pdf'.")

# GUI Setup
root = tk.Tk()
root.title("Print TC")
root.state('zoomed')

tk.Label(root, text="Ready to print Transfer Certificates", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Generate TC", command=generate, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()