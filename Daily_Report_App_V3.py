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
root.geometry("500x600")

# Content Text Area for entering new content
tk.Label(root, text="Enter Content:").pack(pady=(10, 0))
content_text = tk.Text(root, height=10, width=45)
content_text.pack()

# Dropdown for predefined directories
tk.Label(root, text="Class:").pack(pady=(10, 0))
selected_dir = tk.StringVar()
selected_dir.set("")  # Default value

dropdown = tk.OptionMenu(root, selected_dir, *PREDEFINED_DIRS.keys())
dropdown.pack()

# Frame for Most Recent File Editing
recent_file_frame = tk.Frame(root)
recent_file_frame.pack(pady=(20, 0), padx=10, fill="x")

# Label for Most Recent File's name
recent_file_name_label = tk.Label(recent_file_frame, text="No file selected", anchor="w")
recent_file_name_label.pack(fill="x")

# Text area to edit the most recent file content
recent_file_text = tk.Text(recent_file_frame, height=10, width=45)
recent_file_text.pack()

# Button for saving the most recent file after modification
def save_recent_file():
    content = recent_file_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Input Error", "Please fill in the content of the file.")
        return

    chosen_key = selected_dir.get()
    if chosen_key == "Custom...":
        target_dir = filedialog.askdirectory(title="Select Custom Directory")
        if not target_dir:
            return  # User cancelled
    else:
        target_dir = PREDEFINED_DIRS[chosen_key]
        if not target_dir.exists():
            messagebox.showerror("Error", f"The selected directory doesn't exist:\n{target_dir}")
            return

    # Save the edited content to the most recent file
    filename = recent_file_name_label.cget("text")  # Use the current file name
    filepath = os.path.join(target_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", f"File saved at:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# Button for saving the most recent file
save_recent_button = tk.Button(recent_file_frame, text="Save Most Recent File", command=save_recent_file)
save_recent_button.pack(pady=10)

# Function to fetch and display the most recent file for the selected directory
def update_most_recent_file():
    chosen_key = selected_dir.get()
    if chosen_key == "Custom...":
        target_dir = filedialog.askdirectory(title="Select Custom Directory")
        if not target_dir:
            recent_file_name_label.config(text="No file selected")
            recent_file_text.delete("1.0", tk.END)
            return
    else:
        target_dir = PREDEFINED_DIRS[chosen_key]
        if not target_dir.exists():
            messagebox.showerror("Error", f"The selected directory doesn't exist:\n{target_dir}")
            recent_file_name_label.config(text="No file selected")
            recent_file_text.delete("1.0", tk.END)
            return

    most_recent_file = None
    most_recent_time = 0

    # Iterate over the files in the directory to find the most recent one
    for entry in os.scandir(target_dir):
        if entry.is_file():
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
                most_recent_file = entry.name
                most_recent_time = mod_time

    # Update the label and text area with the most recent file found
    if most_recent_file:
        recent_file_name_label.config(text=most_recent_file)
        
        # Read the content of the most recent file into the recent_file_text widget
        with open(target_dir / most_recent_file, "r", encoding="utf-8") as f:
            recent_file_text.delete("1.0", tk.END)  # Clear existing content
            recent_file_text.insert("1.0", f.read())  # Insert the content of the most recent file
    else:
        recent_file_name_label.config(text="No file selected")
        recent_file_text.delete("1.0", tk.END)

# Call this function when the selected directory changes
def on_directory_change(*args):
    update_most_recent_file()

# Bind the dropdown change event to update the most recent file
selected_dir.trace("w", on_directory_change)

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

    most_recent_file = None
    most_recent_time = 0

    # Iterate over the files in the directory using os.scandir
    for entry in os.scandir(target_dir):
        if entry.is_file():
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
                most_recent_file = entry.name
                most_recent_time = mod_time

    # Generate filename and save
    filename = f"{directory_label}.txt"
    filepath = os.path.join(target_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", f"File saved at:\n{filepath}")
        update_most_recent_file()  # Refresh to show the updated file
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# Save Button for the new content
tk.Button(root, text="Save to File", command=save_file).pack(pady=10)

root.mainloop()
