import subprocess
import sys
import importlib.util
import tkinter as tk
from tkinter import messagebox

# Required modules
required_modules = ["customtkinter", "Pillow"]

# Function to check and install
def check_and_install():
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            label_var.set(f"Installing: {module}")
            window.update_idletasks()
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.CalledProcessError:
                messagebox.showerror("Installation Error", f"Failed to install {module}. Please try manually.")
                window.destroy()
                sys.exit(1)

    label_var.set("All dependencies installed!")
    window.after(1000, launch_main_app)

# Function to launch main Git GUI
def launch_main_app():
    window.destroy()
    import github  # <-- replace with the filename of your actual main app, without `.py`

# Setup tkinter setup page
window = tk.Tk()
window.geometry("500x200")
window.title("Setting Up")
window.configure(bg="#2e003e")
window.resizable(False, False)

label_var = tk.StringVar()
label = tk.Label(window, textvariable=label_var, font=("Calibri", 18, "bold"),
                 fg="#ffcc00", bg="#2e003e")
label.pack(expand=True)

label_var.set("Checking dependencies...")
window.after(100, check_and_install)
window.mainloop()
