import tkinter as tk
from tkinter import messagebox
import client

def show_video_management(root, video_management_frame):
    clear_frames(root)
    video_management_frame.pack(fill='both', expand=True)

def show_user_management(root, user_management_frame):
    clear_frames(root)
    user_management_frame.pack(fill='both', expand=True)

def show_comment_management(root, comment_management_frame):
    clear_frames(root)
    comment_management_frame.pack(fill='both', expand=True)

def show_login(root, login_frame):
    clear_frames(root)
    login_frame.pack(fill='both', expand=True)

def show_welcome(root, welcome_frame):
    clear_frames(root)
    welcome_frame.pack(fill='both', expand=True)

def quit_app(root):
    root.destroy()

def clear_frames(root):
    for widget in root.winfo_children():
        widget.pack_forget()

def perform_login(root, login_frame, welcome_frame, username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Warning", "Username and password cannot be empty.")
        return
    if client.login(username, password):  # 假设client.login是验证用户名和密码的函数
        messagebox.showinfo("Login", "Login successful!")
        login_frame.pack_forget()
        welcome_frame.pack(fill='both', expand=True)
    else:
        messagebox.showerror("Login failed", "The username or password is incorrect.")

def perform_create_user(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Warning", "Username and password cannot be empty.")
        return
    if client.create_user(username, password):
        messagebox.showinfo("Success", "User created successfully.")
def show_frame(root, frame_name):
    clear_frames(root)
    frames = {
        'login_frame': root.login_frame,
        'welcome_frame': root.welcome_frame,

        'video_management_frame': root.video_management_frame,
        'user_management_frame': root.user_management_frame,
        'comment_management_frame': root.comment_management_frame,

        'upload_video_frame': root.upload_video_frame,
        'search_video_by_ID': root.search_video_by_ID_frame,
        'search_video_by_keywords': root.search_video_by_keywords_frame,
        'list_videos': root.list_videos_frame,
        'download_video': root.download_video_frame,
        'update_video': root.update_video_frame,
        'delete_video': root.delete_video_frame,

        'search_user_by_id_frame': root.search_user_by_id_frame,
        'search_user_by_keyword_frame': root.search_user_by_keyword_frame,
        'list_all_users_frame': root.list_all_users_frame,
        'update_user_frame': root.update_user_frame


    }
    frame = frames.get(frame_name)
    if frame:
        frame.pack(fill='both', expand=True)
    else:
        messagebox.showerror("Error", "Frame not found: " + frame_name)

def back_to_welcome(root):
    show_frame(root, 'welcome_frame')
def populate_users_text_area(root, users_data):
    # Logic to populate the users text area
    text_area = root.user_management_frame.text_area  # Assuming the text area widget is stored in the frame
    text_area.delete('1.0', tk.END)
    for user in users_data:
        text_area.insert(tk.END, f"User ID: {user['id']}, Name: {user['name']}\n")



