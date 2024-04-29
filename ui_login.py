import tkinter as tk
from tkinter import messagebox
from controllers import perform_login, perform_create_user, show_welcome, show_login, quit_app
import client

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

    # Login Button
    login_button = tk.Button(login_frame, text="Log in",
                             command=lambda: perform_login(root, login_frame, welcome_frame, username_entry, password_entry))
    login_button.pack(pady=10)

    # Create User Button
    create_button = tk.Button(login_frame, text="Create Account",
                              command=lambda: perform_create_user(username_entry.get(), password_entry.get()))
    create_button.pack(pady=10)

    # Exit Button
    exit_button = tk.Button(login_frame, text="Exit", command=lambda: quit_app(root))
    exit_button.pack(pady=10)

# Assuming perform_create_user calls your client method to create a user
def perform_create_user(username, password):
    # This should ideally call your client method or directly the API if needed
    if client.create_user(username, password):
        messagebox.showinfo("Success", "User created successfully")
    else:
        messagebox.showerror("Error", "Failed to create user")

# Assuming your client.create_user looks something like this:
import requests

API_BASE_URL = "http://127.0.0.1:5000"

def create_user(username, password):
    response = requests.post(f"{API_BASE_URL}/create_user", json={'username': username, 'password': password})
    if response.status_code == 201:
        try:
            response_data = response.json()
            if 'error' in response_data:
                return False, response_data['error']
            else:
                return True, "User created successfully"
        except ValueError:
            return False, "Response is not in JSON format"
    else:
        return False, f"Failed to create user, status code: {response.status_code}"
