import customtkinter as ctk
from tkinter import messagebox
from logic.person_ops import persons, delete_person_list
from ui.view import view_person
from ui.form import open_form
import os
import shutil


# ===== DELETE FUNCTION =====
def delete_person(pid, refresh):
    confirm = messagebox.askyesno("Confirm", "Delete this person?")
    if not confirm:
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

    main = ctk.CTkFrame(content)
    main.pack(fill="both", expand=True, padx=15, pady=15)

    # ===== TITLE =====
    ctk.CTkLabel(main,
                 text="📊 Dashboard",
                 font=("Segoe UI", 22, "bold")
    ).pack(pady=10)

    # ===== ADD BUTTON =====
    ctk.CTkButton(main,
                  text="➕ Add Person",
                  command=lambda:
                  open_form(root, content, show_dashboard)
    ).pack(pady=10)

    # ===== CARD CONTAINER =====
    card_container = ctk.CTkFrame(main)
    card_container.pack(fill="both", expand=True)

    if not persons:
        ctk.CTkLabel(card_container,
                     text="No persons found",
                     font=("Segoe UI", 14)
        ).pack(pady=20)
        return

    # ===== CARD GRID =====
    row_frame = None

    for i, (pid, name) in enumerate(persons):

        # New row every 2 cards
        if i % 2 == 0:
            row_frame = ctk.CTkFrame(card_container)
            row_frame.pack(fill="x", pady=5)

        # ===== CARD =====
        card = ctk.CTkFrame(row_frame, width=300, height=150)
        card.pack(side="left", padx=10, pady=10, expand=True)

        # Name
        ctk.CTkLabel(card,
                     text=f"👤 {name}",
                     font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # ID
        ctk.CTkLabel(card,
                     text=f"ID: {pid}",
                     font=("Segoe UI", 12)
        ).pack(anchor="w", padx=10)

        # ===== BUTTON ROW =====
        btn_frame = ctk.CTkFrame(card)
        btn_frame.pack(fill="x", pady=10)

        # VIEW
        ctk.CTkButton(btn_frame,
                      text="View",
                      width=70,
                      command=lambda pid=pid:
                      view_person(root, content, pid, show_dashboard)
        ).pack(side="left", padx=10)

        # DELETE
        ctk.CTkButton(btn_frame,
                      text="Delete",
                      width=70,
                      fg_color="red",
                      hover_color="#aa0000",
                      command=lambda pid=pid:
                      delete_person(pid,
                                    lambda: show_dashboard(root, content))
        ).pack(side="right", padx=10)