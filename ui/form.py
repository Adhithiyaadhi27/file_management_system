import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from utils.helpers import generate_id
from logic.file_ops import save_json
from logic.person_ops import add_person
import os
import shutil


def open_form(root, content, show_dashboard):

    # ===== CLEAR SCREEN =====
    for w in content.winfo_children():
        w.destroy()

    frame = ctk.CTkFrame(content)
    frame.pack(fill="both", expand=True)

    # ===== SCROLL =====
    canvas = ctk.CTkCanvas(frame)
    inner = ctk.CTkFrame(canvas)

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    ))

    # ===== BACK =====
    ctk.CTkButton(inner, text="⬅ Back",
                  command=lambda: show_dashboard(root, content)
    ).pack(pady=5)

    entries = {}

    # ===== FIELD =====
    def add(parent, label, field_type="text", options=None):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", pady=3, padx=5)

        ctk.CTkLabel(row, text=label, width=220).pack(side="left", padx=5)

        if field_type == "text":
            e = ctk.CTkEntry(row)
            e.pack(side="right", fill="x", expand=True)
            entries[label] = e

        elif field_type == "dropdown":
            var = ctk.StringVar()
            ctk.CTkOptionMenu(row, variable=var, values=options).pack(side="right")
            entries[label] = var

        elif field_type == "file":
            var = ctk.StringVar()

            btn = ctk.CTkButton(row, text="Upload")

            def upload():
                f = filedialog.askopenfilename()
                if f:
                    filename = os.path.basename(f)
                    var.set(filename)
                    var.full_path = f
                    btn.configure(text="Uploaded ✓", fg_color="green")

            btn.configure(command=upload)
            btn.pack(side="right", padx=5)

            def open_file():
                if hasattr(var, "full_path"):
                    os.startfile(var.full_path)

            ctk.CTkButton(row,
                          textvariable=var,
                          fg_color="transparent",
                          text_color="#4da6ff",
                          command=open_file
            ).pack(side="right")

            entries[label] = var

    # ===== SECTION =====
    def section(title):
        container = ctk.CTkFrame(inner)
        container.pack(fill="x", pady=5)

        header = ctk.CTkButton(container, text=f"▶ {title}", anchor="w")
        header.pack(fill="x")

        body = ctk.CTkFrame(container)
        body.pack(fill="x")
        body.pack_forget()

        def toggle():
            if body.winfo_ismapped():
                body.pack_forget()
                header.configure(text=f"▶ {title}")
            else:
                body.pack(fill="x")
                header.configure(text=f"▼ {title}")

        header.configure(command=toggle)
        return body

    # ===== ALL SECTIONS =====

    # 13.1 Personal
    sec = section("Personal Details")
    add(sec, "Full Name")
    add(sec, "Father’s Name")
    add(sec, "Date of Birth")
    add(sec, "Marital Status", "dropdown", ["Single", "Married"])
    add(sec, "Spouse Name")
    add(sec, "Nationality")
    add(sec, "Qualification")
    add(sec, "Height")
    add(sec, "Weight")
    add(sec, "Aadhaar Number")

    # 13.2 Family
    sec = section("Family Details")
    add(sec, "Number of Children")
    add(sec, "Children DOB")
    add(sec, "Father’s Age")
    add(sec, "Mother’s Age")
    add(sec, "Spouse Age")
    add(sec, "Brother’s Age")
    add(sec, "Sister’s Age")

    # 13.3 Professional
    sec = section("Professional Details")
    add(sec, "Employer / Business Name")
    add(sec, "Designation")
    add(sec, "Nature of Business")
    add(sec, "Annual Income")

    # 13.4 Contact
    sec = section("Contact Details")
    add(sec, "Office Contact Number")
    add(sec, "Mobile Number 1")
    add(sec, "Mobile Number 2")
    add(sec, "Email ID")

    # 13.5 Identity
    sec = section("Identity Details")
    add(sec, "PAN Number")
    add(sec, "Aadhaar Number")

    # 13.6 Additional
    sec = section("Additional Details")
    add(sec, "Wedding Anniversary")

    # 13.7 Nominee
    sec = section("Nominee Details")
    add(sec, "Nominee Relationship", "dropdown",
        ["Father", "Mother", "Spouse", "Children", "Appointee"])
    add(sec, "Nominee Name")
    add(sec, "Nominee DOB")
    add(sec, "Nominee Father’s Name")

    # 13.8 Insurance
    sec = section("Insurance Details")
    for p in ["Self", "Father", "Mother", "Spouse", "Children"]:
        for f in ["Policy Number", "Sum Assured", "Year of Issue", "Company"]:
            add(sec, f"{p} {f}")

    # 13.9 Health
    sec = section("Health Details")
    add(sec, "Health problems")
    add(sec, "Lifestyle habits")
    add(sec, "Pregnancy details")
    add(sec, "Other remarks")

    # 13.10 Address
    sec = section("Address Details")
    add(sec, "Communication Address")
    add(sec, "Permanent Address")

    # 13.11 Plan
    sec = section("Plan Details")
    add(sec, "Product Name")
    add(sec, "Premium")
    add(sec, "Mode", "dropdown", ["Yearly", "Half-yearly", "Quarterly"])
    add(sec, "Sum Assured")
    add(sec, "Rider")

    # 13.12 Documents
    sec = section("Document Attachments")
    docs = [
        "Age Proof", "ID Proof", "Address Proof", "Photo",
        "School ID", "Form 16", "Bank Statement",
        "Bank Cheque 1", "Bank Cheque 2",
        "Proposal Form 1", "Proposal Form 2",
        "Visiting Card"
    ]
    for d in docs:
        add(sec, d, "file")

    # 13.13 References
    sec = section("References")
    add(sec, "Friend’s Name")
    add(sec, "Mobile Number")
    add(sec, "Age")

    # 13.14 Financial
    sec = section("PAN & Financial Details")
    add(sec, "PAN Number")
    add(sec, "PAN Card Copy", "file")
    add(sec, "Risk Cover")
    add(sec, "Pension Plan")
    add(sec, "Investment Plan")
    add(sec, "Mutual Fund")
    add(sec, "Mediclaim")
    add(sec, "Money Back Policy")
    add(sec, "Children’s Education Plan")
    add(sec, "Reminder Date 1")
    add(sec, "Reminder Date 2")

    # ===== SAVE =====
    def save():
        data = {}

        pid = generate_id()
        person_folder = os.path.join("data", pid)
        files_folder = os.path.join(person_folder, "files")

        os.makedirs(files_folder, exist_ok=True)

        for k, v in entries.items():
            if hasattr(v, "full_path"):
                filename = os.path.basename(v.full_path)
                shutil.copy(v.full_path, os.path.join(files_folder, filename))
                data[k] = filename
            else:
                data[k] = v.get()

        data["ID"] = pid

        if "Date of Birth" in data:
            try:
                data["Age"] = datetime.now().year - int(data["Date of Birth"][:4])
            except:
                pass

        save_json(os.path.join(person_folder, "data.json"), data)
        add_person(pid, data.get("Full Name", "Unknown"))

        messagebox.showinfo("Saved", "Person Added Successfully")
        show_dashboard(root, content)

    ctk.CTkButton(inner, text="💾 Save", command=save).pack(pady=15)