import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from controllers import show_frame, quit_app
API_BASE_URL = 'http://127.0.0.1:5000'

def setup_upload_video_frame(root, upload_video_frame):
    upload_video_label = tk.Label(upload_video_frame, text="Upload a Video", font=("Arial", 20))
    upload_video_label.pack(pady=30)

    title_label = tk.Label(upload_video_frame, text="Title")
    title_label.pack()
    title_entry = tk.Entry(upload_video_frame)
    title_entry.pack(pady=5)

    upload_username_label = tk.Label(upload_video_frame, text="Username")
    upload_username_label.pack()
    upload_username_entry = tk.Entry(upload_video_frame)
    upload_username_entry.pack(pady=5)

    video_path_label = tk.Label(upload_video_frame, text="Video File Path")
    video_path_label.pack()
    video_path_entry = tk.Entry(upload_video_frame)
    video_path_entry.pack(pady=5)

    browse_button = tk.Button(upload_video_frame, text="Browse...", command=lambda: browse_video_file(video_path_entry))
    browse_button.pack(pady=5)

    duration_label = tk.Label(upload_video_frame, text="Duration (seconds)")
    duration_label.pack()
    duration_entry = tk.Entry(upload_video_frame)
    duration_entry.pack(pady=5)

    upload_button = tk.Button(upload_video_frame, text="Upload Video", command=lambda: perform_video_upload(title_entry, upload_username_entry, video_path_entry, duration_entry))
    upload_button.pack(pady=10)

    # Back to comment management button
    back_to_update_button = tk.Button(upload_video_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_update_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(upload_video_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)

def browse_video_file(video_path_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    video_path_entry.delete(0, tk.END)
    video_path_entry.insert(0, file_path)

def perform_video_upload(title_entry, upload_username_entry, video_path_entry, duration_entry):
    title = title_entry.get()
    username = upload_username_entry.get()
    video_path = video_path_entry.get()
    duration = duration_entry.get()

    if not title or not username or not video_path or not duration:
        messagebox.showwarning("Warning", "All fields must be filled out to upload.")
        return

    try:
        with open(video_path, 'rb') as video:
            files = {'video': (video_path, video, 'video/mp4')}
            data = {'title': title, 'username': username, 'duration': duration}
            response = requests.post(f"{API_BASE_URL}/upload_video", files=files, data=data)
            if response.status_code == 202:
                messagebox.showinfo("Success", "Video uploaded successfully!")
            else:
                result = response.json()
                messagebox.showerror("Upload Failed", result.get('error', 'Unknown error occurred.'))
    except FileNotFoundError:
        messagebox.showerror("Error", "Video file not found at specified path.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
