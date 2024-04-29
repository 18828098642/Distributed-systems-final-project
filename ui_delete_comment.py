import tkinter as tk
from tkinter import messagebox
from client import delete_comment
from controllers import show_frame,quit_app
def setup_delete_comment_frame(root, frame):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Title Label
    title_label = tk.Label(frame, text="Delete a Comment", font=("Arial", 16))
    title_label.pack(pady=10)

    # Entry for Comment ID
    comment_id_label = tk.Label(frame, text="Comment ID:")
    comment_id_label.pack()
    comment_id_entry = tk.Entry(frame, width=25)
    comment_id_entry.pack(pady=5)

    # Button to delete the comment
    def on_delete_click():
        comment_id = comment_id_entry.get()
        if not comment_id:
            messagebox.showerror("Error", "Comment ID is required!")
            return
        result = delete_comment(comment_id)
        if isinstance(result, dict):
            messagebox.showinfo("Success", f"Comment Deleted")
        else:
            messagebox.showinfo("Success", f"Comment Deleted")

    delete_button = tk.Button(frame, text="Delete Comment", command=on_delete_click)
    delete_button.pack(pady=20)
    # Back to user management button
    back_button = tk.Button(frame, text="Back to Comment Management", command=lambda: show_frame(root, 'comment_management_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    # Exit system button
    exit_button = tk.Button(frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)