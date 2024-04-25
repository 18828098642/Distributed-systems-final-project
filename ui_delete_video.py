import tkinter as tk
from tkinter import messagebox
import client
from controllers import show_frame, quit_app

def setup_delete_video_frame(root, delete_video_frame):
    # Use grid for more controlled layout
    delete_video_frame.grid_columnconfigure(0, weight=1)  # This makes the column expandable

    # Label for the frame title
    delete_video_label = tk.Label(delete_video_frame, text="Delete Video by ID", font=("Arial", 20))
    delete_video_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Label and entry for video ID
    video_id_label = tk.Label(delete_video_frame, text="Video ID:")
    video_id_label.grid(row=1, column=0, padx=10, sticky="w")

    video_id_entry = tk.Entry(delete_video_frame)
    video_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Delete button
    delete_button = tk.Button(delete_video_frame, text="Delete Video", command=lambda: delete_video(video_id_entry))
    delete_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    # Back to Video Management button
    back_to_video_management_button = tk.Button(delete_video_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_video_management_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    exit_search_video_id_frame_button = tk.Button(delete_video_frame, text="Exit System", command=root.quit)
    exit_search_video_id_frame_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    return delete_video_frame


def delete_video(video_id_entry):
    video_id = video_id_entry.get().strip()
    if not video_id:
        messagebox.showerror("Error", "Video ID is required.")
        return

    try:
        int(video_id)  # Check if video_id is an integer
    except ValueError:
        messagebox.showerror("Error", "Video ID must be a numeric integer.")
        return

    result = client.delete_video(video_id)  # Call to client function to delete video
    if 'error' in result:
        messagebox.showerror("Deletion Failed", result['error'])
    else:
        messagebox.showinfo("Success", "Video deleted successfully from OSS and SQL database.")
