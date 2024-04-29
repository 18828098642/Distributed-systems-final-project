import tkinter as tk
from controllers import show_frame, back_to_welcome, quit_app

def setup_comment_management_frame(root, comment_management_frame):
    # Title Label
    comment_management_label = tk.Label(comment_management_frame, text="Comment Management", font=("Arial", 20))
    comment_management_label.pack(pady=30)

    # Container Frame for Buttons
    comment_buttons_frame = tk.Frame(comment_management_frame)
    comment_buttons_frame.pack(pady=10)

    # Button to post a comment
    post_comment_button = tk.Button(comment_buttons_frame, text="Post a Comment",
                                    command=lambda: show_frame(root, 'post_comment_frame'))
    post_comment_button.pack(fill='x', pady=5)

    # Button to find a comment by ID
    find_comment_id_button = tk.Button(comment_buttons_frame, text="Find a Comment by ID",
                                       command=lambda: show_frame(root, 'find_comment_by_id_frame'))
    find_comment_id_button.pack(fill='x', pady=5)

    # Button to find a comment by keywords
    find_comment_keyword_button = tk.Button(comment_buttons_frame, text="Find a Comment by Keywords",
                                            command=lambda: show_frame(root, 'find_comment_by_keyword_frame'))
    find_comment_keyword_button.pack(fill='x', pady=5)

    # Button to list all comments
    list_all_comments_button = tk.Button(comment_buttons_frame, text="List All Comments",
                                         command=lambda: show_frame(root, 'list_all_comments_frame'))
    list_all_comments_button.pack(fill='x', pady=5)

    # Button to update a comment
    update_comment_button = tk.Button(comment_buttons_frame, text="Update a Comment",
                                      command=lambda: show_frame(root, 'update_comment_frame'))
    update_comment_button.pack(fill='x', pady=5)

    # Button to delete a comment
    delete_comment_button = tk.Button(comment_buttons_frame, text="Delete a Comment",
                                      command=lambda: show_frame(root, 'delete_comment_frame'))
    delete_comment_button.pack(fill='x', pady=5)

    # Navigation and exit buttons
    comment_management_back_button = tk.Button(comment_management_frame, text="Back to last page",
                                               command=lambda: back_to_welcome(root))
    comment_management_back_button.pack(side='left', padx=10, pady=20)

    comment_management_exit_button = tk.Button(comment_management_frame, text="Exit System",
                                               command=lambda: quit_app(root))
    comment_management_exit_button.pack(side='right', padx=10, pady=20)
