import tkinter as tk
from tkinter import scrolledtext, messagebox
from controllers import show_frame, quit_app
import client

def format_json(data, indent=0):
    formatted_text = ""
    if isinstance(data, dict):
        for key, value in data.items():
            formatted_text += "    " * indent + f"{key}: "
            if isinstance(value, dict):
                formatted_text += "\n" + format_json(value, indent + 1)
            elif isinstance(value, list):
                formatted_text += "\n" + format_json(value, indent + 1)
            else:
                formatted_text += f"{value}\n"
    elif isinstance(data, list):
        for item in data:
            formatted_text += format_json(item, indent)
    else:
        formatted_text += f"{'    ' * indent}{data}\n"
    return formatted_text

def setup_list_all_users_frame(root, list_all_users_frame):
    # Clear any existing content in the frame
    for widget in list_all_users_frame.winfo_children():
        widget.destroy()

    # Add title label
    list_users_label = tk.Label(list_all_users_frame, text="List of All Users", font=("Arial", 20))
    list_users_label.pack(pady=20)

    # Create and set up a scrolling text area to display user data
    users_text_area = scrolledtext.ScrolledText(list_all_users_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
    users_text_area.pack(pady=10)

    # Define a function to display all users
    def show_all_users():
        try:
            users = client.list_all_users()  # Fetches the current list of users
            formatted_json = format_json(users)  # Format the user data using the custom formatter
            users_text_area.config(state='normal')
            users_text_area.delete('1.0', tk.END)
            users_text_area.insert(tk.END, formatted_json)  # Display the formatted JSON in the text area
            users_text_area.config(state='disabled')
        except Exception as e:
            messagebox.showerror("List Error", str(e))

    # Refresh list button
    refresh_button = tk.Button(list_all_users_frame, text="Refresh List", command=show_all_users)
    refresh_button.pack(pady=10)

    # Back to user management button
    back_button = tk.Button(list_all_users_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(list_all_users_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)

    return list_all_users_frame
