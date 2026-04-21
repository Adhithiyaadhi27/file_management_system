import customtkinter as ctk
from tkinter import messagebox
from logic.file_ops import load_json, save_json
from utils.helpers import simple_input
from logic.person_ops import update_person
from tkcalendar import Calendar
from datetime import datetime
import os


# ===== CALENDAR POPUP =====
def open_calendar(root, current_value, set_value):

    top = ctk.CTkToplevel(root)
    top.title("Select Date")
    top.geometry("300x320")

    # 🔥 bring to front
    top.transient(root)
    top.grab_set()
    top.focus_force()
    top.lift()

    cal = Calendar(top, date_pattern="dd/mm/yyyy")
    cal.pack(pady=10, fill="both", expand=True)

    # Set existing date if available
    try:
        day, month, year = current_value.split("/")
        cal.selection_set(datetime(int(year), int(month), int(day)))
    except:
        pass

    def select():
        set_value(cal.get_date())
        top.destroy()

    ctk.CTkButton(top, text="Select", command=select).pack(pady=10)


# ===== VIEW =====
def view_person(root, content, pid, show_dashboard):

    # CLEAR SCREEN
    for w in content.winfo_children():
        w.destroy()

    frame = ctk.CTkFrame(content)
    frame.pack(fill="both", expand=True)

    person_folder = os.path.join("data", pid)
    file_name = os.path.join(person_folder, "data.json")

    data = load_json(file_name)

    if not data:
        messagebox.showerror("Error", "Data not found")
        return

    # ===== HEADER =====
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(header,
                 text=f"👤 {pid}",
                 font=("Segoe UI", 20, "bold")
    ).pack(side="left", padx=10)

    ctk.CTkButton(header,
                  text="⬅ Back",
                  command=lambda: show_dashboard(root, content)
    ).pack(side="right", padx=10)

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

    # ===== SCROLL SMOOTH =====
    def on_mousewheel(event):
        canvas.yview_scroll(int(-event.delta / 60), "units")

    inner.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    inner.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # ===== DATA DISPLAY =====
    for key, value in data.items():

        row = ctk.CTkFrame(inner)
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row,
                     text=key,
                     width=200,
                     anchor="w",
                     font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        val_label = ctk.CTkLabel(row, text=str(value))
        val_label.pack(side="left", padx=5)

        # ===== EDIT FUNCTION =====
        def make_edit(k, label):

            def edit_field():

                date_fields = [
                    "Date of Birth",
                    "Wedding Anniversary",
                    "Nominee DOB",
                    "DOB of each child"
                ]

                # ===== DATE FIELD =====
                if k in date_fields:

                    def set_date(new_val):
                        data[k] = new_val
                        save_json(file_name, data)
                        label.configure(text=new_val)

                    open_calendar(root, data.get(k, ""), set_date)

                # ===== NORMAL FIELD =====
                else:
                    new_val = simple_input(root, f"Edit {k}")

                    if new_val:
                        data[k] = new_val
                        save_json(file_name, data)
                        label.configure(text=new_val)

                        # Update dashboard if name changes
                        if k == "Full Name":
                            update_person(pid, new_val)
                            show_dashboard(root, content)

            return edit_field

        ctk.CTkButton(
            row,
            text="✏",
            width=40,
            command=make_edit(key, val_label)
        ).pack(side="right")