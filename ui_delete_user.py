import tkinter as tk
from tkinter import messagebox
import client
from controllers import show_frame, quit_app

def setup_delete_user_frame(root, delete_user_frame):
    # Use grid for more controlled layout
    delete_user_frame.grid_columnconfigure(0, weight=1)  # Make the column expandable

    # Label for the frame title
    delete_user_label = tk.Label(delete_user_frame, text="Delete User by ID", font=("Arial", 20))
    delete_user_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Label and entry for user ID
    user_id_label = tk.Label(delete_user_frame, text="User ID:")
    user_id_label.grid(row=1, column=0, padx=10, sticky="w")

    user_id_entry = tk.Entry(delete_user_frame)
    user_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Delete button
    delete_button = tk.Button(delete_user_frame, text="Delete User", command=lambda: delete_user(user_id_entry))
    delete_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Back to User Management button
    back_to_user_management_button = tk.Button(delete_user_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_to_user_management_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    exit_button = tk.Button(delete_user_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    return delete_user_frame

def delete_user(user_id_entry):
    user_id = user_id_entry.get().strip()
    if not user_id:
        messagebox.showerror("Error", "User ID is required.")
        return

    try:
        int(user_id)  # Check if user_id is an integer
    except ValueError:
        messagebox.showerror("Error", "User ID must be a numeric integer.")
        return

    result = client.delete_user(user_id)  # Call to client function to delete user
    if result is None:
        messagebox.showinfo("Success", "User deleted successfully.")
    elif 'error' in result:
        messagebox.showerror("Deletion Failed", result['error'])
    else:
        messagebox.showinfo("Success", "User deleted successfully.")

