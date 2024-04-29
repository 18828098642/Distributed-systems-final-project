import tkinter as tk
from tkinter import messagebox
from client import post_comment
from controllers import show_frame, quit_app
from config import API_BASE_URL
import requests
def setup_post_comment_frame(root, frame):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Title Label
    title_label = tk.Label(frame, text="Post a Comment", font=("Arial", 16))
    title_label.pack(pady=10)

    # Entry for Video ID
    video_id_label = tk.Label(frame, text="Video ID:")
    video_id_label.pack()
    video_id_entry = tk.Entry(frame, width=25)
    video_id_entry.pack(pady=5)

    # Entry for User ID
    user_id_label = tk.Label(frame, text="User ID:")
    user_id_label.pack()
    user_id_entry = tk.Entry(frame, width=25)
    user_id_entry.pack(pady=5)

    # Entry for Comment Text
    comment_text_label = tk.Label(frame, text="Comment Text:")
    comment_text_label.pack()
    comment_text_entry = tk.Entry(frame, width=25)
    comment_text_entry.pack(pady=5)

    def post_comment(video_id, user_id, comment_text):
        url = f"{API_BASE_URL}/post_comment"
        data = {
            'video_id': video_id,
            'user_id': user_id,
            'comment_text': comment_text
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()  # Assume the API always responds with JSON
        except requests.HTTPError as e:
            return {'error': f'HTTP Error: {e.response.status_code} {e.response.reason}'}
        except requests.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}
        except ValueError:
            return {'error': 'Invalid response from server, not JSON.'}
    # Function to handle button click and post the comment
    def on_post_click():
        video_id = video_id_entry.get()
        user_id = user_id_entry.get()
        comment_text = comment_text_entry.get()
        if not video_id or not user_id or not comment_text:
            messagebox.showerror("Error", "All fields are required!")
            return
        result = post_comment(video_id, user_id, comment_text)
        if 'error' in result:
            messagebox.showerror("Error", result['error'])
        elif 'message' in result:
            messagebox.showinfo("Success", result['message'])
        else:
            messagebox.showerror("Error", "Unexpected error occurred")

    # Button to post the comment
    post_button = tk.Button(frame, text="Post Comment", command=on_post_click)
    post_button.pack(pady=20)

    # Back to comment management button
    back_button = tk.Button(frame, text="Back to Comment Management", command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)
