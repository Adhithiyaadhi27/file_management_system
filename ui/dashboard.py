import tkinter as tk
from logic.person_ops import persons
from ui.view import view_person
from ui.form import open_form
import os

def delete_person(pid, show_dashboard):
    import os
    from logic.person_ops import delete_person_list

    # delete file
    file_name = f"{pid}.json"
    if os.path.exists(file_name):
        os.remove(file_name)

    # delete from list
    delete_person_list(pid)

    # refresh UI
    show_dashboard()

def show_dashboard(root, content):
    for w in content.winfo_children():
        w.destroy()

    for pid, name in persons:
        row = tk.Frame(content)
        row.pack(fill="x")

        tk.Label(row, text=f"{pid} - {name}").pack(side="left")

        tk.Button(row, text="View",
                  command=lambda pid=pid: view_person(root, pid,
                                                      lambda: show_dashboard(root, content))
        ).pack(side="right")

        tk.Button(row, text="Delete",
                  command=lambda pid=pid: delete_person(
                        pid,
                        lambda: show_dashboard(root, content)
                    )
        ).pack(side="right")

    tk.Button(content, text="Add",
              command=lambda: open_form(root,
                                       lambda: show_dashboard(root, content))
    ).pack()