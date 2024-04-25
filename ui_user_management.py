import tkinter as tk
from controllers import show_frame, back_to_welcome, quit_app, populate_users_text_area

def setup_user_management_frame(root, user_management_frame):
    # Title Label
    user_management_label = tk.Label(user_management_frame, text="User Management", font=("Arial", 20))
    user_management_label.pack(pady=30)

    # Container Frame for Buttons
    user_buttons_frame = tk.Frame(user_management_frame)
    user_buttons_frame.pack(pady=10)

    # Button to search users by ID
    search_user_by_id_button = tk.Button(user_buttons_frame, text="Search a User by ID",
                                         command=lambda: show_frame(root, 'search_user_by_id_frame'))
    search_user_by_id_button.pack(fill='x', pady=5)

    # Button to search users by keywords
    search_by_keyword_button = tk.Button(user_buttons_frame, text="Search a User by Keywords",
                                         command=lambda: show_frame(root, 'search_user_by_keyword_frame'))
    search_by_keyword_button.pack(fill='x', pady=5)

    # Button to list all users
    list_all_users_button = tk.Button(user_buttons_frame, text="List All Users",
                                      command=lambda: populate_users_text_area())
    list_all_users_button.pack(fill='x', pady=5)

    # Button to update user information
    update_user_information_button = tk.Button(user_buttons_frame, text="Update User Information",
                                               command=lambda: show_frame(root, 'update_user_frame'))
    update_user_information_button.pack(fill='x', pady=5)

    # Navigation and exit buttons
    user_management_back_button = tk.Button(user_management_frame, text="Back to last page",
                                            command=lambda: back_to_welcome(root))
    user_management_back_button.pack(side='left', padx=10, pady=20)

    user_management_exit_button = tk.Button(user_management_frame, text="Exit System",
                                            command=lambda: quit_app(root))
    user_management_exit_button.pack(side='right', padx=10, pady=20)
