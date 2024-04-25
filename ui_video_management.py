import tkinter as tk
from tkinter import messagebox, filedialog
from controllers import show_frame, back_to_welcome, quit_app

def setup_video_management_frame(root, video_management_frame):
    video_management_label = tk.Label(video_management_frame, text="Video Management", font=("Arial", 20))
    video_management_label.pack(pady=30)

    video_buttons_frame = tk.Frame(video_management_frame)
    video_buttons_frame.pack(pady=10)

    upload_video_button = tk.Button(video_buttons_frame, text="Upload a Video", command=lambda: show_frame(root, 'upload_video_frame'))
    upload_video_button.pack(fill='x', pady=5)

    search_video_id_button = tk.Button(video_buttons_frame, text="Search a Video by ID",
                                       command=lambda: show_frame(root, 'search_video_by_ID'))
    search_video_id_button.pack(fill='x', pady=5)

    search_video_id_button = tk.Button(video_buttons_frame, text="Search a Video by Keywords",
                                       command=lambda: show_frame(root, 'search_video_by_keywords'))
    search_video_id_button.pack(fill='x', pady=5)

    search_video_id_button = tk.Button(video_buttons_frame, text="List all Videos",
                                       command=lambda: show_frame(root, 'list_videos'))
    search_video_id_button.pack(fill='x', pady=5)

    search_video_id_button = tk.Button(video_buttons_frame, text="Download a Video",
                                       command=lambda: show_frame(root, 'download_video'))
    search_video_id_button.pack(fill='x', pady=5)

    update_video_button = tk.Button(video_buttons_frame, text="Update Video", command=lambda: show_frame(root, 'update_video'))
    update_video_button.pack(fill='x', pady=5)

    delete_video_button = tk.Button(video_buttons_frame, text="Delete Video", command=lambda: show_frame(root, 'delete_video'))
    delete_video_button.pack(fill='x', pady=5)

    video_management_back_button = tk.Button(video_management_frame, text="Back to last page", command=lambda: back_to_welcome(root))
    video_management_back_button.pack(side='left', padx=10, pady=20)

    video_management_exit_button = tk.Button(video_management_frame, text="Exit System", command=lambda: quit_app(root))
    video_management_exit_button.pack(side='right', padx=10, pady=20)
