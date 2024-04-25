import tkinter as tk
from tkinter import messagebox, scrolledtext
import client  # Assuming the client module can interact with the backend.
from controllers import show_frame, back_to_welcome, quit_app, populate_users_text_area
def setup_list_all_users_frame(root, list_users_frame):
    # Frame configuration for list all users
    list_users_label = tk.Label(list_users_frame, text="List of All Users", font=("Arial", 20))
    list_users_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # ScrolledText area for displaying all users
    users_text_area = scrolledtext.ScrolledText(list_users_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
    users_text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Function to populate the text area with user details
    def populate_users_text_area():
        try:
            users = client.list_all_users()
            users_text_area.config(state='normal')
            users_text_area.delete('1.0', tk.END)
            if 'error' in users:
                messagebox.showerror("Error", users['error'])
            else:
                for user in users:
                    users_text_area.insert(tk.END, f"ID: {user['id']}, Username: {user['username']}\n")
                    users_text_area.insert(tk.END, "Comments:\n")
                    for comment in user['comments']:
                        users_text_area.insert(tk.END, f"  - {comment['text']} (Comment ID {comment['id']})\n")
                    users_text_area.insert(tk.END, "Videos:\n")
                    for video in user['videos']:
                        users_text_area.insert(tk.END, f"  - {video['title']} (Video ID {video['id']})\n")
                    users_text_area.insert(tk.END, "-" * 80 + "\n")  # Separator for readability
            users_text_area.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    # Button to refresh and list all users
    refresh_users_button = tk.Button(list_users_frame, text="Refresh List", command=populate_users_text_area)
    refresh_users_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Back button to return to the user management page
    back_to_user_management_button = tk.Button(list_users_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_to_user_management_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    # Exit button to exit the system
    exit_list_users_frame_button = tk.Button(list_users_frame, text="Exit System", command=lambda: quit_app(root))
    exit_list_users_frame_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    return list_users_frame
