import uuid
import tkinter as tk

def generate_id():
    return str(uuid.uuid4())[:8]

def simple_input(root, title):
    p = tk.Toplevel(root)
    tk.Label(p, text=title).pack()
    e = tk.Entry(p)
    e.pack()

    val = {"v": None}

    def submit():
        val["v"] = e.get()
        p.destroy()

    tk.Button(p, text="OK", command=submit).pack()
    root.wait_window(p)
    return val["v"]