import tkinter as tk
from controllers import show_frame, back_to_welcome, quit_app

def setup_comment_management_frame(root, comment_management_frame):
    comment_management_label = tk.Label(comment_management_frame, text="Comment Management", font=("Arial", 20))
    comment_management_label.pack(pady=30)

    comment_buttons_frame = tk.Frame(comment_management_frame)
    comment_buttons_frame.pack(pady=10)

    post_comment_button = tk.Button(comment_buttons_frame, text="Post a Comment")
    post_comment_button.pack(fill='x', pady=5)

    find_comment_id_button = tk.Button(comment_buttons_frame, text="Find a Comment by ID")
    find_comment_id_button.pack(fill='x', pady=5)

    find_comment_keyword_button = tk.Button(comment_buttons_frame, text="Find a Comment by Keywords")
    find_comment_keyword_button.pack(fill='x', pady=5)

    list_all_comments_button = tk.Button(comment_buttons_frame, text="List All Comments")
    list_all_comments_button.pack(fill='x', pady=5)

    update_comment_button = tk.Button(comment_buttons_frame, text="Update a Comment")
    update_comment_button.pack(fill='x', pady=5)

    delete_comment_button = tk.Button(comment_buttons_frame, text="Delete a Comment")
    delete_comment_button.pack(fill='x', pady=5)

    comment_management_back_button = tk.Button(comment_management_frame, text="Back to last page", command=lambda: back_to_welcome(root))
    comment_management_back_button.pack(side='left', padx=10, pady=20)

    comment_management_exit_button = tk.Button(comment_management_frame, text="Exit System", command=lambda: quit_app(root))
    comment_management_exit_button.pack(side='right', padx=10, pady=20)
