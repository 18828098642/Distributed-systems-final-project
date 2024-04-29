import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from controllers import show_frame, quit_app
from config import API_BASE_URL

def get_comment_details(comment_id):
    response = requests.get(f"{API_BASE_URL}/comment_details", params={'comment_id': comment_id})
    try:
        comment_details = response.json()
        if 'error' not in comment_details:
            return comment_details
        else:
            return {'error': comment_details['error']}
    except ValueError:
        return {'error': "Response is not in JSON format"}

def setup_find_comment_by_id_frame(root, frame):
    frame.grid_columnconfigure(1, weight=1)

    title_label = tk.Label(frame, text="Search a Comment by ID", font=("Arial", 20))
    title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

    comment_id_label = tk.Label(frame, text="Comment ID:")
    comment_id_label.grid(row=1, column=0, padx=10, sticky="e")
    comment_id_entry = tk.Entry(frame)
    comment_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    comments_text = scrolledtext.ScrolledText(frame, width=70, height=15, wrap=tk.WORD, state='disabled')
    comments_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def on_search_click():
        comment_id = comment_id_entry.get().strip()
        if not comment_id:
            messagebox.showerror("Error", "Comment ID is required!")
            return

        comment = get_comment_details(comment_id)  # 调用函数获取评论详情
        comments_text.config(state=tk.NORMAL)
        comments_text.delete('1.0', tk.END)

        if 'error' not in comment:
            # 将评论详情格式化为字符串，并插入到文本框中
            comment_details = (f"Comment ID: {comment.get('id', 'N/A')}, Text: {comment.get('comment_text', 'N/A')}\n"
                               f"Created At: {comment.get('created_at', 'N/A')}\n"
                               f"Commenter ID: {comment.get('user_id', 'N/A')}\n\n")
            comments_text.insert(tk.END, comment_details)
        else:
            # 如果发生错误，显示错误消息
            comments_text.insert(tk.END, comment.get('error', 'No comment found for this ID.'))

        comments_text.config(state='disabled')

    search_button = tk.Button(frame, text="Search", command=on_search_click)
    search_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    back_button = tk.Button(frame, text="Back to Comment Management", command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    exit_button = tk.Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.grid(row=4, column=1, padx=10, pady=20, sticky="e")

    return frame
