import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext, Tk, Label, Button
from controllers import show_frame, quit_app
from config import API_BASE_URL

def list_all_comments():
    response = requests.get(f"{API_BASE_URL}/list_all_comments")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve comments"}  # 返回错误信息

def setup_list_all_comments_frame(root, frame):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Title Label
    title_label = Label(frame, text="List All Comments", font=("Arial", 16))
    title_label.pack(pady=10)

    # Scrolled Text Widget for displaying comments
    comments_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, width=50)
    comments_text.pack(padx=10, pady=10)

    # Function to refresh comments list
    def refresh_comments():
        comments_text.config(state='normal')  # Enable text widget for editing
        comments_text.delete('1.0', tk.END)  # Clear existing text
        comments = list_all_comments()
        if isinstance(comments, list):
            for comment in comments:
                comments_text.insert(tk.END, f"Comment ID: {comment['id']}, Video ID: {comment['video_id']}, User ID: {comment['user_id']}\n")
                comments_text.insert(tk.END, f"Comment: {comment['comment_text']}, Created at: {comment['created_at']}\n")
                comments_text.insert(tk.END, "-" * 40 + "\n")
        else:
            messagebox.showerror("Error", comments.get('error', 'An unexpected error occurred'))
        comments_text.config(state='disabled')  # Disable editing again

    # Button to refresh the comments list
    refresh_button = Button(frame, text="Refresh Comments", command=refresh_comments)
    refresh_button.pack(pady=10)

    back_button = Button(frame, text="Back to Comment Management", command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)

