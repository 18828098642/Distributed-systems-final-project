import tkinter as tk
from tkinter import scrolledtext, messagebox
from controllers import show_frame, show_video_management, quit_app
import client

def setup_list_videos_frame(root, list_videos_frame):
    list_videos_label = tk.Label(list_videos_frame, text="List of All Videos", font=("Arial", 20))
    list_videos_label.pack(pady=30)

    videos_text_area = scrolledtext.ScrolledText(list_videos_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
    videos_text_area.pack(pady=10)

    def populate_videos_text_area(videos):
        videos_text_area.config(state='normal')
        videos_text_area.delete('1.0', tk.END)
        if 'error' in videos:
            messagebox.showerror("Error", videos['error'])
        else:
            for video in videos:
                videos_text_area.insert(tk.END, f"ID: {video['id']}, Title: {video['title']}, Author: {video['author']}\n")
                videos_text_area.insert(tk.END, f"Path: {video['video_path']}, Size: {video['bytes']} bytes\n")
                videos_text_area.insert(tk.END, f"Duration: {video['duration_seconds']} seconds, Uploaded at: {video['upload_time']}\n")
                videos_text_area.insert(tk.END, "-" * 80 + "\n")  # Separator for readability
        videos_text_area.config(state='disabled')

    def show_all_videos():
        try:
            videos = client.list_all_videos()
            populate_videos_text_area(videos)
        except Exception as e:
            messagebox.showerror("List Error", str(e))

    refresh_button = tk.Button(list_videos_frame, text="Refresh List", command=show_all_videos)
    refresh_button.pack(pady=10)


    back_to_video_management_button = tk.Button(list_videos_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_video_management_button.pack(side='left', padx=10, pady=20)

    exit_search_keywords_frame_button = tk.Button(list_videos_frame, text="Exit System", command=root.quit)
    exit_search_keywords_frame_button.pack(side='right', padx=10, pady=20)

    return list_videos_frame
