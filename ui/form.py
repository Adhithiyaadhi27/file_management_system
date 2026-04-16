import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from utils.helpers import generate_id
from logic.file_ops import save_json
from logic.person_ops import add_person


def open_form(root, show_dashboard):
    win = tk.Toplevel(root)
    win.title("Add Person")
    win.geometry("600x700")

    # ===== SCROLL SETUP =====
    canvas = tk.Canvas(win)
    frame = tk.Frame(canvas)

    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    ))

    def enable_super_smooth_scroll(canvas, frame):

        scroll_speed = 1  # adjust speed here (1 = slow, 2–3 = fast)

        def on_mousewheel(event):
            delta = int(-event.delta / 120)
            canvas.yview_scroll(delta * scroll_speed, "units")

        def on_shift_mousewheel(event):
            delta = int(-event.delta / 120)
            canvas.xview_scroll(delta * scroll_speed, "units")

        # Activate only when mouse inside
        frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Horizontal scroll (Shift + wheel)
        frame.bind("<Shift-MouseWheel>", on_shift_mousewheel)

        # Linux support
        frame.bind("<Button-4>", lambda e: canvas.yview_scroll(-1 * scroll_speed, "units"))
        frame.bind("<Button-5>", lambda e: canvas.yview_scroll(1 * scroll_speed, "units"))

    # ===== SMOOTH SCROLL =====
    def on_mousewheel(event):
        canvas.yview_scroll(int(-event.delta / 60), "units")

    frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    frame.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    frame.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    entries = {}
    entry_order = []

    # ===== SECTION =====
    def section(title):
        tk.Label(frame, text=title,
                 bg="#2f3640", fg="white",
                 font=("Segoe UI", 11, "bold")
        ).pack(fill="x", pady=5)

    # ===== ADD FIELD =====
    def add(label, field_type="text", options=None):
        row = tk.Frame(frame)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=label, width=25, anchor="w").pack(side="left")

        if field_type == "text":
            e = tk.Entry(row)
            e.pack(side="right", fill="x", expand=True)

            entry_order.append(e)

            def focus_next(event):
                idx = entry_order.index(e)
                if idx < len(entry_order) - 1:
                    entry_order[idx + 1].focus()

            e.bind("<Return>", focus_next)

            entries[label] = e

        elif field_type == "dropdown":
            var = tk.StringVar()
            tk.OptionMenu(row, var, *options).pack(side="right")
            entries[label] = var

        elif field_type == "file":
            var = tk.StringVar()

            def upload():
                f = filedialog.askopenfilename()
                if f:
                    var.set(f)

            tk.Button(row, text="Upload", command=upload).pack(side="right")
            entries[label] = var

    # ===== FORM CONTENT =====
    section("👤 Personal Details")
    add("Full Name")
    add("Father’s Name")
    add("Date of Birth")
    add("Marital Status", "dropdown", ["Single", "Married"])
    add("Spouse Name")
    add("Nationality")
    add("Qualification")
    add("Height")
    add("Weight")
    add("Aadhaar Number")

    section("👨‍👩‍👧 Family Details")
    add("Number of Children")
    add("Children DOB")
    add("Father’s Age")
    add("Mother’s Age")
    add("Spouse Age")
    add("Brother’s Age")
    add("Sister’s Age")

    section("💼 Professional Details")
    add("Employer / Business Name")
    add("Designation")
    add("Nature of Business")
    add("Annual Income")

    section("📞 Contact Details")
    add("Office Contact Number")
    add("Mobile Number 1")
    add("Mobile Number 2")
    add("Email ID")

    section("🆔 Identity Details")
    add("PAN Number")
    add("Aadhaar Number")

    section("💍 Additional Details")
    add("Wedding Anniversary")

    section("🧾 Nominee Details")
    add("Nominee Relationship", "dropdown",
        ["Father", "Mother", "Spouse", "Children", "Appointee"])
    add("Nominee Name")
    add("Nominee DOB")
    add("Nominee Father’s Name")

    section("🛡 Insurance Details")
    for p in ["Self", "Father", "Mother", "Spouse", "Children"]:
        for f in ["Policy Number", "Sum Assured", "Year of Issue", "Company"]:
            add(f"{p} {f}")

    section("🏥 Health Details")
    add("Health problems")
    add("Lifestyle habits")
    add("Pregnancy details")
    add("Other remarks")

    section("🏠 Address Details")
    add("Communication Address")
    add("Permanent Address")

    section("📋 Plan Details")
    add("Product Name")
    add("Premium")
    add("Mode", "dropdown", ["Yearly", "Half-yearly", "Quarterly"])
    add("Sum Assured")
    add("Rider")

    section("📎 Document Attachments")
    for doc in [
        "Age Proof", "ID Proof", "Address Proof", "Photo",
        "School ID", "Form 16", "Bank Statement",
        "Bank Cheque 1", "Bank Cheque 2",
        "Proposal Form 1", "Proposal Form 2",
        "Visiting Card"
    ]:
        add(doc, "file")

    section("👥 References")
    add("Friend’s Name")
    add("Mobile Number")
    add("Age")

    section("🪪 PAN & Financial Details")
    add("PAN Number")
    add("PAN Card Copy", "file")

    add("Risk Cover")
    add("Pension Plan")
    add("Investment Plan")
    add("Mutual Fund")
    add("Mediclaim")
    add("Money Back Policy")
    add("Children’s Education Plan")

    add("Reminder Date 1")
    add("Reminder Date 2")

    # ===== SAVE =====
    def save():
        data = {}

        for k, v in entries.items():
            data[k] = v.get()

        pid = generate_id()
        data["ID"] = pid

        # Auto age
        if "Date of Birth" in data:
            try:
                data["Age"] = datetime.now().year - int(data["Date of Birth"][:4])
            except:
                pass

        save_json(f"{pid}.json", data)
        add_person(pid, data.get("Full Name", "Unknown"))

        messagebox.showinfo("Saved", "Person Added Successfully")

        win.destroy()
        show_dashboard()

    tk.Button(frame, text="💾 Save",
              bg="green", fg="white",
              command=save).pack(pady=15)