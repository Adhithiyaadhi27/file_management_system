import tkinter as tk
from tkinter import messagebox
from logic.file_ops import load_json, save_json
from utils.helpers import simple_input
from logic.person_ops import update_person


def view_person(root, pid, show_dashboard):
    file_name = f"{pid}.json"
    data = load_json(file_name)

    if not data:
        messagebox.showerror("Error", "Data not found")
        return

    # ===== WINDOW =====
    win = tk.Toplevel(root)
    win.title(f"View - {pid}")
    win.geometry("600x700")

    # ===== SCROLLABLE FRAME =====
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

    # ===== SMOOTH SCROLL =====
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Only scroll when cursor inside frame
    frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Linux scroll support
    frame.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    frame.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ===== DATA DISPLAY =====
    for key, value in data.items():
        row = tk.Frame(frame)
        row.pack(fill="x", padx=10, pady=2)

        tk.Label(row,
                 text=key,
                 width=25,
                 anchor="w",
                 font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        val_label = tk.Label(row, text=value, anchor="w")
        val_label.pack(side="left", padx=5)

        # ===== EDIT FIELD FUNCTION =====
        def make_edit(k, label):
            def edit_field():
                new_val = simple_input(root, f"Edit {k}")
                if new_val:
                    data[k] = new_val
                    save_json(file_name, data)
                    label.config(text=new_val)

                    # Update dashboard if name changes
                    if k == "Full Name":
                        update_person(pid, new_val)
                        show_dashboard()
            return edit_field

        tk.Button(row,
                  text="✏",
                  command=make_edit(key, val_label)
        ).pack(side="right")