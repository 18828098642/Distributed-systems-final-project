import tkinter as tk
from controllers import perform_login, perform_create_user, show_welcome, show_login, quit_app
from controllers import show_frame
def setup_welcome_frame(root, welcome_frame):
    welcome_label = tk.Label(welcome_frame, text="Welcome!", font=("Arial", 20))
    welcome_label.pack(pady=30)

    buttons_frame = tk.Frame(welcome_frame)
    buttons_frame.pack()

    manage_videos_button = tk.Button(buttons_frame, text="Manage Videos", command=lambda: show_frame(root, 'video_management_frame'))
    manage_videos_button.pack(fill='x')

    manage_users_button = tk.Button(buttons_frame, text="Manage Users", command=lambda: show_frame(root, 'user_management_frame'))
    manage_users_button.pack(fill='x', pady=5)

    manage_comments_button = tk.Button(buttons_frame, text="Manage Comments", command=lambda: show_frame(root, 'comment_management_frame'))
    manage_comments_button.pack(fill='x')

    back_button = tk.Button(welcome_frame, text="Back to login", command=lambda: show_frame(root, 'login_frame'))
    back_button.pack(side='left', padx=10, pady=20)

    exit_button = tk.Button(welcome_frame, text="Exit System", command=lambda: quit_app(root))
    exit_button.pack(side='right', padx=10, pady=20)

