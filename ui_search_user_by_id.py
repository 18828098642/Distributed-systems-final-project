import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import client
from controllers import show_frame, quit_app

def setup_search_user_by_id_frame(root, delete_video_frame):
    # Search User by ID frame setup
    search_user_by_id_frame = tk.Frame(root)
    search_user_by_id_label = tk.Label(search_user_by_id_frame, text="Search a User by ID", font=("Arial", 20))
    search_user_by_id_label.pack(pady=30)

    # Entry for the user ID
    user_id_label = tk.Label(search_user_by_id_frame, text="User ID:")
    user_id_label.pack()
    user_id_entry = tk.Entry(search_user_by_id_frame)
    user_id_entry.pack(pady=5)

    # Text area for displaying user details
    user_details_text = scrolledtext.ScrolledText(search_user_by_id_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
    user_details_text.pack(pady=10)

    # Function to display user details
    def display_user_details(user_info):
        user_details_text.config(state='normal')
        user_details_text.delete('1.0', tk.END)
        if 'error' in user_info:
            messagebox.showerror("Error", user_info['error'])
        else:
            user_details_text.insert('1.0', f"User ID: {user_info['id']}\nUsername: {user_info['username']}\n")
            user_details_text.insert(tk.END, "\nComments:\n")
            for comment in user_info['comments']:
                user_details_text.insert(tk.END, f"  - {comment['text']} (Video ID {comment['video_id']})\n")
            user_details_text.insert(tk.END, "\nVideos:\n")
            for video in user_info['videos']:
                user_details_text.insert(tk.END, f"  - {video['title']} (Video ID {video['id']})\n")
        user_details_text.config(state='disabled')

    # Button to search for the user
    def perform_user_search():
        user_id = user_id_entry.get()
        if not user_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric user ID.")
            return
        try:
            user_info = client.get_user_info(user_id)
            display_user_details(user_info)
        except requests.exceptions.HTTPError as http_err:
            # Check if the exception is a 404 Not Found error
            if http_err.response.status_code == 404:
                messagebox.showerror("Search Error", "User with the provided ID not found.")
            else:
                messagebox.showerror("Search Error", f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Search Error", f"An error occurred: {err}")
        except Exception as e:
            messagebox.showerror("Search Error", f"An unexpected error occurred: {e}")

    search_user_button = tk.Button(search_user_by_id_frame, text="Search User", command=perform_user_search)
    search_user_button.pack(pady=10)

    # Back button to return to the user management page
    back_to_user_management_button = tk.Button(search_user_by_id_frame, text="Back to User Management", command=lambda: show_frame(root, 'user_management_frame'))
    back_to_user_management_button.pack(side='left', padx=10, pady=20)

    # Exit button to exit the system
    exit_search_user_frame_button = tk.Button(search_user_by_id_frame, text="Exit System", command=lambda: quit_app(root))
    exit_search_user_frame_button.pack(side='right', padx=10, pady=20)

    return search_user_by_id_frame

