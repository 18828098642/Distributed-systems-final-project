import tkinter as tk
from tkinter import messagebox
import client  # Ensure this module exists and is accessible

def setup_search_user_by_keywords_frame(root,search_user_by_keywords_frame):
    search_video_id_label = tk.Label(search_user_by_keywords_frame, text="Search Video by ID", font=("Arial", 20))
    search_video_id_label.pack(pady=30)

    keyword_label = tk.Label(search_user_by_keywords_frame, text="Keyword:")
    keyword_label.pack()
    keyword_entry = tk.Entry(search_user_by_keywords_frame)
    keyword_entry.pack(pady=5)

    listbox = tk.Listbox(search_user_by_keywords_frame, width=70, height=15)
    listbox.pack(pady=10)

    def perform_search():
        keyword = keyword_entry.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword to search.")
            return
        try:
            # Assuming client.search_users_by_keyword is an existing function that fetches user data
            users = client.search_users_by_keyword(keyword)
            listbox.delete(0, tk.END)
            for user in users:
                listbox.insert(tk.END, f"User ID: {user['id']}, Username: {user['username']}")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    search_button = tk.Button(search_user_by_keywords_frame, text="Search Users", command=perform_search)
    search_button.pack(pady=10)

    return search_user_by_keywords_frame
