import tkinter as tk
from tkinter import messagebox
import client
from controllers import show_frame, quit_app

def setup_update_video_frame(root, update_video_frame):
    # Function to call the update_video_title from client module
    def update_video():
        video_id = video_id_entry.get().strip()
        new_title = new_title_entry.get().strip()
        if not video_id or not new_title:
            messagebox.showerror("Error", "Both video ID and new title are required.")
            return

        try:
            int(video_id)  # Check if video_id is an integer
        except ValueError:
            messagebox.showerror("Error", "Video ID must be a numeric integer.")
            return

        result = client.update_video_title(video_id, new_title)
        if result and 'error' in result:
            messagebox.showerror("Update Failed", result['error'])
        elif result:
            messagebox.showinfo("Success", "Video title updated successfully!")
        else:
            messagebox.showerror("Update Failed", "No response received from server.")

    # Setup for Update Video Frame
    update_video_label = tk.Label(update_video_frame, text="Update Video Information", font=("Arial", 20))
    update_video_label.pack(pady=20)

    # Entry for Video ID
    video_id_label = tk.Label(update_video_frame, text="Video ID:")
    video_id_label.pack()
    video_id_entry = tk.Entry(update_video_frame)
    video_id_entry.pack(pady=5)

    # Entry for New Title
    new_title_label = tk.Label(update_video_frame, text="New Title:")
    new_title_label.pack()
    new_title_entry = tk.Entry(update_video_frame)
    new_title_entry.pack(pady=5)

    # Button to submit the update
    update_button = tk.Button(update_video_frame, text="Update Video", command=update_video)
    update_button.pack(pady=20)

    back_to_update_button = tk.Button(update_video_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_update_button.pack(side='left', padx=10, pady=20)

    exit_update_button = tk.Button(update_video_frame, text="Exit System", command=root.quit)
    exit_update_button.pack(side='right', padx=10, pady=20)