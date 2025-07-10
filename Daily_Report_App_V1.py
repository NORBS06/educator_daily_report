import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Create the main window
root = tk.Tk()
root.title("Form to File Saver")
root.geometry("400x300")

# Labels and Inputs
tk.Label(root, text="Directory Label (used for filename):").pack(pady=(10, 0))
dir_label_entry = tk.Entry(root, width=40)
dir_label_entry.pack()

tk.Label(root, text="Enter Content:").pack(pady=(10, 0))
content_text = tk.Text(root, height=10, width=40)
content_text.pack()

def save_file():
    directory_label = dir_label_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()

    if not directory_label or not content:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    # Let user choose the target directory
    target_dir = filedialog.askdirectory(title="Select Save Directory")
    if not target_dir:
        return  # User canceled

    # Create file path
    filename = f"{directory_label}_data.txt"
    filepath = os.path.join(target_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", f"File saved at:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# Save Button
save_button = tk.Button(root, text="Save to File", command=save_file)
save_button.pack(pady=10)

# Run the app
root.mainloop()
