import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Frame, scrolledtext
import requests
from config import API_BASE_URL
from controllers import show_frame, quit_app

def setup_find_comment_by_keyword_frame(root, frame):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Title Label
    title_label = Label(frame, text="Find Comments by Keyword", font=("Arial", 16))
    title_label.pack(pady=10)

    # Entry for Keyword
    keyword_label = Label(frame, text="Keyword:")
    keyword_label.pack()
    keyword_entry = Entry(frame, width=50)
    keyword_entry.pack(pady=5)

    # Scrolled Text Widget for displaying comments
    comments_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, width=50)
    comments_text.pack(padx=10, pady=10)
    comments_text.config(state=tk.DISABLED)  # Disable editing of the content

    def search_comments(keyword):
        """Fetches comments based on a keyword from API."""
        response = requests.get(f"{API_BASE_URL}/search_comments", params={'keyword': keyword})
        try:
            return response.json()
        except ValueError:
            return {"error": "Response is not in JSON format"}

    def on_search_click():
        keyword = keyword_entry.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Keyword is required!")
            return

        comments = search_comments(keyword)
        comments_text.config(state=tk.NORMAL)
        comments_text.delete('1.0', tk.END)  # Clear the text widget

        if 'error' in comments:
            messagebox.showerror("Error", comments['error'])
            comments_text.insert(tk.END, comments['error'])
        else:
            for comment in comments:
                comment_details = (f"Comment ID: {comment['comment_id']}, Text: {comment['text']}\n"
                                   f"Created At: {comment['created_at']}, Video Title: {comment['video_title']}\n"
                                   f"Commenter ID: {comment['commenter_id']}, Commenter Username: {comment['commenter_username']}\n\n")
                comments_text.insert(tk.END, comment_details)

        comments_text.config(state=tk.DISABLED)

    # Button to search the comments
    search_button = Button(frame, text="Search", command=on_search_click)
    search_button.pack(pady=10)

    # Back to comment management button
    back_button = tk.Button(frame, text="Back to Comment Management",
                            command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)

