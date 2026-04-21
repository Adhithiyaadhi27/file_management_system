import customtkinter as ctk
from tkinter import messagebox
from logic.person_ops import persons, delete_person_list
from ui.view import view_person
from ui.form import open_form
from datetime import datetime
import os
import shutil
import json


NOTIF_FILE = "data/notifications.json"


# ===== LOAD / SAVE =====
def load_notifications():
    if not os.path.exists(NOTIF_FILE):
        return []
    try:
        with open(NOTIF_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_notifications(data):
    os.makedirs("data", exist_ok=True)
    with open(NOTIF_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ===== DATE HELPER =====
def get_next_dob_date(dob):
    today = datetime.now()
    day, month, year = dob.split("/")

    dob_date = datetime(today.year, int(month), int(day))

    if dob_date < today:
        dob_date = datetime(today.year + 1, int(month), int(day))

    return dob_date


# ===== STORE NOTIFICATIONS =====
def update_notifications():

    today = datetime.now()
    notifications = load_notifications()

    if not os.path.exists("data"):
        return notifications

    updated_notifications = []

    for pid in os.listdir("data"):

        file_path = os.path.join("data", pid, "data.json")

        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            name = data.get("Full Name", "Unknown")
            dob = data.get("Date of Birth")

            if dob:
                msg = f"{name} birthday on {dob}"

                # Check if already exists → update
                found = False

                for n in notifications:
                    if n["msg"].startswith(name + " birthday"):
                        n["msg"] = msg
                        found = True
                        updated_notifications.append(n)
                        break

                # If not found → add new
                if not found:
                    updated_notifications.append({
                        "msg": msg,
                        "date": str(today.date())
                    })

        except:
            continue

    # Replace old list
    save_notifications(updated_notifications)

    return updated_notifications


# ===== UPCOMING DOB =====
def get_upcoming_birthdays_list():

    today = datetime.now()
    upcoming = []

    if not os.path.exists("data"):
        return []

    for pid in os.listdir("data"):

        file_path = os.path.join("data", pid, "data.json")

        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            name = data.get("Full Name", "Unknown")
            dob = data.get("Date of Birth")

            if dob:
                next_dob = get_next_dob_date(dob)
                diff = (next_dob - today).days

                if 0 <= diff <= 7:
                    upcoming.append((name, dob, diff))

        except:
            continue

    upcoming.sort(key=lambda x: x[2])
    return upcoming


# ===== NOTIFICATION UI =====
def show_notifications_ui(root, content):

    for w in content.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(content, corner_radius=15)
    main.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkFrame(main, fg_color="transparent")
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(header,
                 text="🔔 Notifications",
                 font=("Segoe UI", 24, "bold")
    ).pack(side="left")

    ctk.CTkButton(header,
                  text="⬅ Back",
                  command=lambda: show_dashboard(root, content)
    ).pack(side="right")

    scroll = ctk.CTkScrollableFrame(main)
    scroll.pack(fill="both", expand=True)

    notifications = load_notifications()

    # SORT BY DOB
    def extract_dob(n):
        try:
            dob = n["msg"].split("on ")[1]
            return get_next_dob_date(dob)
        except:
            return datetime.max

    notifications.sort(key=extract_dob)

    if not notifications:
        ctk.CTkLabel(scroll, text="No notifications 🎉").pack(pady=20)
        return

    for n in notifications:

        card = ctk.CTkFrame(scroll, corner_radius=12)
        card.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(card,
                     text=n["msg"]).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(card,
                     text=n["date"],
                     text_color="gray").pack(anchor="w", padx=10)


# ===== DELETE =====
def delete_person(pid, refresh):
    if not messagebox.askyesno("Confirm", "Delete this person?"):
        return

    folder = os.path.join("data", pid)
    if os.path.exists(folder):
        shutil.rmtree(folder)

    delete_person_list(pid)
    refresh()


# ===== DASHBOARD =====
def show_dashboard(root, content):

    for w in content.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(content, corner_radius=15)
    main.pack(fill="both", expand=True, padx=20, pady=20)

    # HEADER
    header = ctk.CTkFrame(main, fg_color="transparent")
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(header,
                 text="📊 Dashboard",
                 font=("Segoe UI", 24, "bold")
    ).pack(side="left")

    right = ctk.CTkFrame(header, fg_color="transparent")
    right.pack(side="right")

    notifications = update_notifications()
    count = len(notifications)

    ctk.CTkButton(
        right,
        text=f"🔔 {count}",
        command=lambda: show_notifications_ui(root, content)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        right,
        text="➕ Add Person",
        command=lambda: open_form(root, content, show_dashboard)
    ).pack(side="left")

    # SEARCH
    search_frame = ctk.CTkFrame(main)
    search_frame.pack(fill="x", pady=15)

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="🔍 Search by name or ID...",
        height=42
    )
    search_entry.pack(fill="x", padx=10, pady=10)

    # ===== UPCOMING TITLE + CARD =====
    upcoming = get_upcoming_birthdays_list()

    if upcoming:

        # TITLE
        ctk.CTkLabel(
            main,
            text="🎂 Upcoming Birthday",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(5, 0))

        name, dob, diff = upcoming[0]

        card = ctk.CTkFrame(main, corner_radius=15)
        card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            card,
            text=name,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        if diff == 0:
            status = "🎉 TODAY"
            color = "#2ecc71"
        elif diff == 1:
            status = "Tomorrow"
            color = "#f39c12"
        else:
            status = f"In {diff} days"
            color = "#3498db"

        ctk.CTkLabel(
            card,
            text=f"{status} • {dob} ({diff} days left)",
            text_color=color,
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=15, pady=(0, 10))

    # ===== PERSON LIST =====
    container = ctk.CTkScrollableFrame(main)
    container.pack(fill="both", expand=True)

    def display_cards(data):

        for w in container.winfo_children():
            w.destroy()

        if not data:
            ctk.CTkLabel(container, text="No persons found").pack(pady=20)
            return

        for pid, name in data:

            card = ctk.CTkFrame(container, corner_radius=12)
            card.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(card,
                         text=f"👤 {name}",
                         font=("Segoe UI", 14, "bold")
            ).pack(anchor="w", padx=10)

            ctk.CTkLabel(card,
                         text=f"ID: {pid}",
                         text_color="gray").pack(anchor="w", padx=10)

            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(fill="x")

            ctk.CTkButton(btns,
                          text="View",
                          command=lambda pid=pid:
                          view_person(root, content, pid, show_dashboard)
            ).pack(side="left", padx=10)

            ctk.CTkButton(btns,
                          text="Delete",
                          fg_color="#e53935",
                          command=lambda pid=pid:
                          delete_person(pid,
                                        lambda: show_dashboard(root, content))
            ).pack(side="right", padx=10)

    def on_search(event=None):
        q = search_entry.get().lower()
        filtered = [(pid, name) for pid, name in persons
                    if q in pid.lower() or q in name.lower()]
        display_cards(filtered)

    search_entry.bind("<KeyRelease>", on_search)

    display_cards(persons)