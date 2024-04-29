import tkinter as tk
from tkinter import messagebox
import client  # Ensure the client module has the method to search users by keyword
from controllers import show_frame, quit_app

def setup_search_user_by_keywords_frame(root, search_user_by_keywords_frame):
    search_user_by_keywords_frame.grid_columnconfigure(1, weight=1)  # Makes the second column expandable

    # Title label
    search_user_by_keywords_label = tk.Label(search_user_by_keywords_frame, text="Search Users by Keyword", font=("Arial", 20))
    search_user_by_keywords_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

    # Entry for keyword
    keyword_label = tk.Label(search_user_by_keywords_frame, text="Keyword:")
    keyword_label.grid(row=1, column=0, padx=10, sticky="e")
    keyword_entry = tk.Entry(search_user_by_keywords_frame)
    keyword_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Listbox for displaying search results
    users_listbox = tk.Listbox(search_user_by_keywords_frame, width=70, height=15)
    users_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Function to update listbox with search results
    def perform_search():
        keyword = keyword_entry.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword to search.")
            return
        try:
            users = client.search_users(keyword)
            users_listbox.delete(0, tk.END)
            for user in users:
                users_listbox.insert(tk.END, f"User ID: {user['id']}, Username: {user['username']}")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    # Button to initiate search
    search_button = tk.Button(search_user_by_keywords_frame, text="Search Users", command=perform_search)
    search_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Back button to user management
    back_button = tk.Button(search_user_by_keywords_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_button.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    # Exit button to exit the system
    exit_button = tk.Button(search_user_by_keywords_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.grid(row=4, column=1, padx=10, pady=20, sticky="e")

    return search_user_by_keywords_frame
