import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from datetime import date

# Get current date
today = date.today()
date_str = today.strftime("%d %b")

# Get system home path
HOME = Path.home()

# Define some common directories (adjust as needed for your system)
PREDEFINED_DIRS = {
    "Grade 7 Red": HOME / "Documents\Labourdonnais_College\Y2025\G7R\log",
    "Grade 10 Almond": HOME / "Documents\Labourdonnais_College\Y2025\G10A\log",
    "Grade 10 Blue": HOME / "Documents\Labourdonnais_College\Y2025\G10B\log",
    "Grade 10 Red": HOME / "Documents\Labourdonnais_College\Y2025\G10R\log",
    "Grade 10 Yellow": HOME / "Documents\Labourdonnais_College\Y2025\G10Y\log",
    "Grade 11 Red": HOME / "Documents\Labourdonnais_College\Y2025\G11R\log",
    "Grade 11 Yellow": HOME / "Documents\Labourdonnais_College\Y2025\G11Y\log",
    "Custom...": None  # We'll handle this separately
}

# Main window
root = tk.Tk()
root.title("Daily Report")
root.geometry("450x350")

# Directory Label Entry
# tk.Label(root, text="Filename Label (used for filename):").pack(pady=(10, 0))
# dir_label_entry = tk.Entry(root, width=45)
# dir_label_entry.pack()

# Content Text Area
tk.Label(root, text="Enter Content:").pack(pady=(10, 0))
content_text = tk.Text(root, height=10, width=45)
content_text.pack()

# Dropdown for predefined directories
tk.Label(root, text="Class:").pack(pady=(10, 0))
selected_dir = tk.StringVar()
selected_dir.set("")  # Default value

dropdown = tk.OptionMenu(root, selected_dir, *PREDEFINED_DIRS.keys())
dropdown.pack()

def save_file():
    directory_label = date_str
    content = content_text.get("1.0", tk.END).strip()

    if not directory_label or not content:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    chosen_key = selected_dir.get()
    if chosen_key == "Custom...":
        target_dir = filedialog.askdirectory(title="Select Custom Save Directory")
        if not target_dir:
            return  # User cancelled
    else:
        target_dir = PREDEFINED_DIRS[chosen_key]
        if not target_dir.exists():
            messagebox.showerror("Error", f"The selected directory doesn't exist:\n{target_dir}")
            return
        
    # Generate filename and save
    filename = f"{directory_label}.txt"
    filepath = os.path.join(target_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", f"File saved at:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# Save Button
tk.Button(root, text="Save to File", command=save_file).pack(pady=10)

root.mainloop()
