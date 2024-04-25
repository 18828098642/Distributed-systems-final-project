import tkinter as tk
from tkinter import messagebox
from controllers import show_frame, quit_app, show_video_management
import client

def setup_search_video_by_keywords_frame(root, search_keywords_frame):
    search_keywords_label = tk.Label(search_keywords_frame, text="Search Videos by Keywords", font=("Arial", 20))
    search_keywords_label.pack(pady=30)

    keyword_label = tk.Label(search_keywords_frame, text="Keyword")
    keyword_label.pack()
    keyword_entry = tk.Entry(search_keywords_frame)
    keyword_entry.pack(pady=5)

    videos_listbox = tk.Listbox(search_keywords_frame, width=70, height=15)
    videos_listbox.pack(pady=10)

    def populate_videos_listbox(videos):
        videos_listbox.delete(0, tk.END)
        if 'error' in videos:
            messagebox.showerror("Error", videos['error'])
        else:
            for video in videos:
                videos_listbox.insert(tk.END, f"ID: {video['id']}, Title: {video['title']}, Author: {video['author']}")

    def perform_video_keyword_search():
        keyword = keyword_entry.get()
        try:
            videos_info = client.search_videos(keyword)
            populate_videos_listbox(videos_info)
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    search_button = tk.Button(search_keywords_frame, text="Search Videos", command=perform_video_keyword_search)
    search_button.pack(pady=10)

    back_to_video_management_button = tk.Button(search_keywords_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_video_management_button.pack(side='left', padx=10, pady=20)

    exit_search_keywords_frame_button = tk.Button(search_keywords_frame, text="Exit System", command=root.quit)
    exit_search_keywords_frame_button.pack(side='right', padx=10, pady=20)

    return search_keywords_frame
