import tkinter as tk
from ui.dashboard import show_dashboard

root = tk.Tk()
root.geometry("900x600")

content = tk.Frame(root)
content.pack(fill="both", expand=True)

show_dashboard(root, content)

root.mainloop()