import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Frame
import requests
from config import API_BASE_URL
from controllers import show_frame, quit_app

def setup_update_comment_frame(root, frame):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Title Label
    title_label = Label(frame, text="Update Comment", font=("Arial", 16))
    title_label.pack(pady=10)

    # Entry for Comment ID
    comment_id_label = Label(frame, text="Comment ID:")
    comment_id_label.pack()
    comment_id_entry = Entry(frame, width=50)
    comment_id_entry.pack(pady=5)

    # Entry for New Content
    new_content_label = Label(frame, text="New Content:")
    new_content_label.pack()
    new_content_entry = Entry(frame, width=50)
    new_content_entry.pack(pady=5)

    # Function to handle the update
    def on_update_click():
        comment_id = comment_id_entry.get().strip()
        new_content = new_content_entry.get().strip()
        if not comment_id or not new_content:
            messagebox.showerror("Error", "Both fields are required!")
            return

        response = requests.post(f"{API_BASE_URL}/update_comment", json={
            'comment_id': comment_id,
            'new_content': new_content
        })

        try:
            result = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", "Comment updated successfully!")
            else:
                messagebox.showerror("Error", result.get('error', "Failed to update comment due to server error."))
        except ValueError:
            messagebox.showerror("Error", "Response is not in JSON format: " + response.text)

    # Button to update the comment
    update_button = Button(frame, text="Update Comment", command=on_update_click)
    update_button.pack(pady=20)

    # Back to user management button
    back_button = tk.Button(frame, text="Back to Comment Management", command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)
