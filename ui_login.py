import tkinter as tk
from controllers import perform_login, perform_create_user, show_welcome, show_login, quit_app
import client
from tkinter import messagebox
# ui_login.py
def setup_login_frame(root, login_frame, welcome_frame):
    title_label = tk.Label(login_frame, text="Video Management System Login", font=("Arial", 16))
    title_label.pack(pady=20)

    username_label = tk.Label(login_frame, text="Username")
    username_label.pack()

    username_entry = tk.Entry(login_frame)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_frame, text="Password")
    password_label.pack()

    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack(pady=5)

    # Assuming perform_login requires the root and frames as arguments
    login_button = tk.Button(login_frame, text="Log in",
                             command=lambda: perform_login(root, login_frame, welcome_frame, username_entry,
                                                           password_entry))
    login_button.pack(pady=10)

