import tkinter as tk
from tkinter import messagebox
from controllers import show_frame
import client

def setup_search_video_by_ID_frame(root, search_video_id_frame):
    search_video_id_label = tk.Label(search_video_id_frame, text="Search Video by ID", font=("Arial", 20))
    search_video_id_label.pack(pady=30)

    video_id_label = tk.Label(search_video_id_frame, text="Video ID")
    video_id_label.pack()
    video_id_entry = tk.Entry(search_video_id_frame)
    video_id_entry.pack(pady=5)

    input_display_label = tk.Label(search_video_id_frame, text="")
    input_display_label.pack()

    def update_input_display(event):
        current_input = video_id_entry.get()
        if current_input.isdigit():
            input_display_label.config(text=f"Current Input: {current_input}")
        else:
            video_id_entry.delete(0, tk.END)
            messagebox.showerror("Invalid Input", "Please enter a numeric value.")
    video_id_entry.bind("<KeyRelease>", update_input_display)

    video_details_listbox = tk.Listbox(search_video_id_frame, width=70, height=15)
    video_details_listbox.pack(pady=10)

    def populate_video_details_listbox(video):
        video_details_listbox.delete(0, tk.END)
        if 'error' in video:
            messagebox.showerror("Error", video['error'])
        else:
            video_details_listbox.insert(tk.END, f"ID: {video['id']}, Title: {video['title']}, Author: {video['author']}")
            video_details_listbox.insert(tk.END, f"Duration: {video['duration_seconds']} seconds")
            video_details_listbox.insert(tk.END, f"Size: {video['size']} bytes")
            video_details_listbox.insert(tk.END, f"Uploaded at: {video['upload_time']}")

    def perform_video_id_search():
        video_id = video_id_entry.get()
        try:
            video = client.get_video_details(int(video_id))
            populate_video_details_listbox(video)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid ID format.")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    search_button = tk.Button(search_video_id_frame, text="Search Video", command=perform_video_id_search)
    search_button.pack(pady=10)

    back_to_video_management_button = tk.Button(search_video_id_frame, text="Back to Video Management", command=lambda: show_frame(root, 'video_management_frame'))
    back_to_video_management_button.pack(side='left', padx=10, pady=20)

    exit_search_video_id_frame_button = tk.Button(search_video_id_frame, text="Exit System", command=root.quit)
    exit_search_video_id_frame_button.pack(side='right', padx=10, pady=20)
