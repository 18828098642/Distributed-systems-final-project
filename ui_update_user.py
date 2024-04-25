import tkinter as tk
from tkinter import messagebox
import client  # Assuming client has the method to update user info
from controllers import show_frame, quit_app

def setup_update_user_frame(root, update_user_frame):
    update_user_frame.grid_columnconfigure(1, weight=1)  # Makes the second column expandable

    # Title label
    update_user_label = tk.Label(update_user_frame, text="Update User Information", font=("Arial", 20))
    update_user_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

    # Entry for User ID
    user_id_label = tk.Label(update_user_frame, text="User ID:")
    user_id_label.grid(row=1, column=0, padx=10, sticky="e")
    user_id_entry = tk.Entry(update_user_frame)
    user_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Entry for New Username
    new_username_label = tk.Label(update_user_frame, text="New Username:")
    new_username_label.grid(row=2, column=0, padx=10, sticky="e")
    new_username_entry = tk.Entry(update_user_frame)
    new_username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Entry for New Password
    new_password_label = tk.Label(update_user_frame, text="New Password:")
    new_password_label.grid(row=3, column=0, padx=10, sticky="e")
    new_password_entry = tk.Entry(update_user_frame, show="*")
    new_password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # Function to handle user update
    def submit_update():
        user_id = user_id_entry.get().strip()
        new_username = new_username_entry.get().strip()
        new_password = new_password_entry.get().strip()
        if not user_id.isdigit():
            messagebox.showerror("Error", "ID must be a numerical value")
            return

        result = client.update_user_info(user_id, new_username, new_password)
        if 'error' in result:
            messagebox.showerror("Failed", result['error'])
        else:
            messagebox.showinfo("Successful", "Updated successfully!")

    # Button to submit the update
    update_button = tk.Button(update_user_frame, text="Update User", command=submit_update)
    update_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Back button to user management
    back_button = tk.Button(update_user_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_button.grid(row=5, column=0, padx=10, pady=20, sticky="w")

    # Exit button to exit the system
    exit_button = tk.Button(update_user_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.grid(row=5, column=1, padx=10, pady=20, sticky="e")

    return update_user_frame
