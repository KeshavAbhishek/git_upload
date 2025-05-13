import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import subprocess
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk

# Setup dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Main app setup
app = ctk.CTk()
app.overrideredirect(True)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")
app.configure(bg="#2e003e")
app.bind("<Escape>", lambda e: app.destroy())

scale = screen_width / 1920  # Responsive font and widget sizing

# Variables
repo_path = ctk.StringVar()
git_username = ctk.StringVar()
git_email = ctk.StringVar()
commit_msg = ctk.StringVar(value="1st-commit")
repo_url = ctk.StringVar()

# Background GitHub Logo
# try:
#     img = Image.open("glogo.png").convert("RGBA")
#     img = img.resize((int(screen_width * 0.6), int(screen_height * 0.6)))
#     img.putalpha(30)  # faint effect

#     background_image = ImageTk.PhotoImage(img)
#     background_label = ctk.CTkLabel(app, image=background_image, text="")
#     background_label.place(relx=0.5, rely=0.5, anchor="center")
# except Exception as e:
#     print("Could not load background image:", e)

# Popup for user input
def popup_input(title, prompt):
    top = ctk.CTkToplevel(app)
    top.geometry("400x200")
    top.title(title)
    top.configure(bg="#2e003e")
    top.grab_set()
    top.result = None

    label = ctk.CTkLabel(top, text=prompt,
                         text_color="#ffcc00", font=("Calibri", 20, "bold"), bg_color="#2e003e")
    label.pack(pady=20)

    entry = ctk.CTkEntry(top, placeholder_text="Enter here", width=250,
                         height=40, text_color="#2e003e", fg_color="#ffcc00")
    entry.pack(pady=10)

    def submit():
        val = entry.get().strip()
        if val:
            top.result = val
            top.destroy()

    submit_btn = ctk.CTkButton(top, text="Submit", command=submit,
                               fg_color="#ffcc00", hover_color="#e6b800",
                               text_color="#2e003e", font=("Calibri", 16, "bold"))
    submit_btn.pack(pady=10)

    top.wait_window()
    return top.result

# Check git config
def check_git_config():
    try:
        username = subprocess.check_output(["git", "config", "--global", "user.name"]).decode().strip()
        email = subprocess.check_output(["git", "config", "--global", "user.email"]).decode().strip()
    except subprocess.CalledProcessError:
        username, email = "", ""

    if not username:
        username = popup_input("Git Username", "Enter your Git user.name")
        if username:
            subprocess.run(["git", "config", "--global", "user.name", username])
    if not email:
        email = popup_input("Git Email", "Enter your Git user.email")
        if email:
            subprocess.run(["git", "config", "--global", "user.email", email])

    git_username.set(username)
    git_email.set(email)

# Git automation logic
def run_git_commands():
    path = repo_path.get()
    user = git_username.get()
    email = git_email.get()
    msg_text = commit_msg.get()
    url = repo_url.get()

    if not all([path, user, email, url]):
        CTkMessagebox(title="Missing Info", message="Please fill all fields (except commit message).",
                          icon="cancel", option_1="OK")
        return

    try:
        os.chdir(path)
        subprocess.run(["git", "config", "--global", "user.name", user], check=True)
        subprocess.run(["git", "config", "--global", "user.email", email], check=True)
        subprocess.run(["git", "config", "--global", "http.postBuffer", "2147483648"], check=True)
        subprocess.run(["git", "config", "--global", "core.packedGitLimit", "1g"], check=True)
        subprocess.run(["git", "config", "--global", "core.packedGitWindowSize", "1g"], check=True)

        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", msg_text], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        CTkMessagebox(title="Success", message="Repository initialized and pushed!",
                          icon="check", option_1="OK")
    except subprocess.CalledProcessError as e:
        CTkMessagebox(title="Git Error", message=str(e), icon="cancel", option_1="OK")
    except Exception as e:
        CTkMessagebox(title="Error", message=str(e), icon="cancel", option_1="OK")

# Browse directory
def browse_path():
    path = askdirectory()
    if path:
        repo_path.set(path)

# Input creator
def add_input(label_text, var, row_index, placeholder):
    spacing = 0.11
    label_font = ("Calibri", int(24 * scale), "bold")
    entry_font = ("Calibri", int(22 * scale), "bold")

    label = ctk.CTkLabel(app, text=label_text, text_color="#ffcc00", font=label_font, bg_color="#2e003e")
    label.place(relx=0.5, rely=0.05 + row_index * spacing, anchor="center")

    entry = ctk.CTkEntry(app, textvariable=var, width=int(650 * scale), height=int(50 * scale),
                         fg_color="#2e003e", text_color="#ffcc00", border_color="#ffcc00",
                         font=entry_font, placeholder_text=placeholder,
                         placeholder_text_color="#888")
    entry.place(relx=0.5, rely=0.05 + (row_index * spacing) + 0.05, anchor="center")

# Inputs
add_input("Repository Path", repo_path, 0, "e.g. C:/Users/You/Projects/my-repo")
browse_btn = ctk.CTkButton(app, text="📁", command=browse_path,
                           fg_color="#4444aa", hover_color="#333388",
                           text_color="white", width=50, height=50,
                           font=("Calibri", int(22 * scale), "bold"))
browse_btn.place(relx=0.84, rely=0.16, anchor="center")

add_input("Git Username", git_username, 1, "e.g. your-username")
add_input("Git Email", git_email, 2, "e.g. your@email.com")
add_input("Commit Message", commit_msg, 3, "e.g. initial commit")
add_input("Repository URL", repo_url, 4, "e.g. https://github.com/user/repo.git")

# Submit button
submit_btn = ctk.CTkButton(app, text="🚀 Initialize & Push",
                           command=run_git_commands,
                           fg_color="#ffcc00", hover_color="#e6b800",
                           text_color="#2e003e",
                           font=("Calibri", int(26 * scale), "bold"),
                           width=int(450 * scale), height=int(60 * scale),
                           corner_radius=12)
submit_btn.place(relx=0.5, rely=0.74, anchor="center")

# Terminate button (below)
terminate_btn = ctk.CTkButton(app, text="✕", command=app.destroy,
                              fg_color="#ff4c4c", hover_color="#e60000",
                              text_color="white", width=int(70 * scale), height=int(70 * scale),
                              corner_radius=35, font=("Arial", int(28 * scale), "bold"))
terminate_btn.place(relx=0.5, rely=0.85, anchor="center")

# Check config on startup
check_git_config()

app.mainloop()
