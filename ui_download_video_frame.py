# ui_download_video_frame.py

import tkinter as tk
from tkinter import messagebox, filedialog
from controllers import show_frame, show_video_management, quit_app
import client

def setup_download_video_frame(root, download_video_frame):
    download_video_label = tk.Label(download_video_frame, text="Download a Video by ID", font=("Arial", 20))
    download_video_label.pack(pady=30)

    video_id_label = tk.Label(download_video_frame, text="Video ID")
    video_id_label.pack()
    video_id_entry = tk.Entry(download_video_frame)
    video_id_entry.pack(pady=5)

    def initiate_download():
        video_id = video_id_entry.get().strip()  # Strip to remove any leading/trailing whitespace
        download_folder = filedialog.askdirectory()

        # Check if the download folder was selected
        if not download_folder:
            messagebox.showerror("Error", "Please choose a download folder.")
            return

        # Check if the video ID is a valid integer
        try:
            int(video_id)  # Attempt to convert to integer to validate
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric video ID.")
            return

        # If all checks pass, proceed with download
        message = client.download_video_by_id(video_id, download_folder)
        messagebox.showinfo("Download", message)

    download_button = tk.Button(download_video_frame, text="Download Video", command=initiate_download)
    download_button.pack(pady=10)

    back_to_video_management_button = tk.Button(download_video_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_video_management_button.pack(side='left', padx=10, pady=20)

    exit_download_frame_button = tk.Button(download_video_frame, text="Exit System", command=lambda: quit_app(root))
    exit_download_frame_button.pack(side='right', padx=10, pady=20)



