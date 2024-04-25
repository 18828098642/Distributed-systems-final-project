import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import client  # Assuming your client code is in a file named client.py
import requests  # 确保导入了requests库
import re
from tkinter import messagebox
API_BASE_URL = 'http://127.0.0.1:5000'

def show_comment_management():
    clear_frames()
    comment_management_frame.pack(fill='both', expand=True)


def show_user_management():
    clear_frames()
    user_management_frame.pack(fill='both', expand=True)


def show_video_management():
    clear_frames()
    video_management_frame.pack(fill='both', expand=True)

# Go back to welcome from video management
def back_to_welcome():
    show_welcome()

def clear_frames():
    for widget in root.winfo_children():
        widget.pack_forget()

def show_login():
    clear_frames()
    login_frame.pack(fill='both', expand=True)

def show_welcome():
    clear_frames()
    welcome_frame.pack(fill='both', expand=True)

def perform_login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Warning", "Username and password cannot be empty.")
        return
    if client.login(username, password):  # 假设这是一个验证用户名和密码的函数
        messagebox.showinfo("Login", "Login successful!")
        login_frame.pack_forget()  # 隐藏登录框
        show_welcome()  # 显示欢迎界面或其他界面
    else:
        messagebox.showerror("Login failed", "The username or password is incorrect.")


def perform_create_user():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Warning", "Username and password cannot be empty.")
        return
    if client.create_user(username, password):
        messagebox.showinfo("Success", "User created successfully.")

def quit_app():
    root.destroy()


# ----------------------------------------------------------------------login create user-------------------------------------------------------------------------------



root = tk.Tk()
root.title("Video Management System")
root.geometry('800x600')

login_frame = tk.Frame(root)
title_label = tk.Label(login_frame, text="Video Management System Login", font=("Arial", 16))
title_label.pack(pady=20)

username_label = tk.Label(login_frame, text="Username")
username_label.pack()

username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password")
password_label.pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Log in", command=perform_login)
login_button.pack(pady=10)

create_user_button = tk.Button(login_frame, text="Create a user", command=perform_create_user)
create_user_button.pack(pady=10)



#------------------------------------------------------------------------Welcome-----------------------------------------------------------------------------



# Welcome frame setup
welcome_frame = tk.Frame(root)
welcome_label = tk.Label(welcome_frame, text="Welcome!", font=("Arial", 20))
welcome_label.pack(pady=30)

# Buttons frame to contain management buttons
buttons_frame = tk.Frame(welcome_frame)
buttons_frame.pack()

# Manage Videos button
manage_videos_button = tk.Button(buttons_frame, text="Manage Videos", command=show_video_management)
manage_videos_button.pack(fill='x')

# Manage Users button
manage_users_button = tk.Button(buttons_frame, text="Manage Users", command=show_user_management)
manage_users_button.pack(fill='x', pady=5)

# Manage Comments button
manage_comments_button = tk.Button(buttons_frame, text="Manage Comments", command=show_comment_management)
manage_comments_button.pack(fill='x')

# Back and Exit buttons
back_button = tk.Button(welcome_frame, text="Back to login", command=show_login)
back_button.pack(side='left', padx=10, pady=20)

exit_button = tk.Button(welcome_frame, text="Exit System", command=quit_app)
exit_button.pack(side='right', padx=10, pady=20)




# ----------------------------------------------------------------------Video management-------------------------------------------------------------------------------


# Video Management frame setup
video_management_frame = tk.Frame(root)
video_management_label = tk.Label(video_management_frame, text="Video Management", font=("Arial", 20))
video_management_label.pack(pady=30)

# This frame will contain all the video management buttons
video_buttons_frame = tk.Frame(video_management_frame)
video_buttons_frame.pack(pady=10)

# Add video management buttons here
upload_video_button = tk.Button(video_buttons_frame, text="Upload a Video", command=lambda: show_frame(upload_video_frame))
upload_video_button.pack(fill='x', pady=5)

search_video_id_button = tk.Button(video_buttons_frame, text="Search a Video by ID")
search_video_id_button.pack(fill='x', pady=5)

search_video_keywords_button = tk.Button(video_buttons_frame, text="Search a Video by Keywords")
search_video_keywords_button.pack(fill='x', pady=5)

list_videos_button = tk.Button(video_buttons_frame, text="List all Videos")
list_videos_button.pack(fill='x', pady=5)

download_video_button = tk.Button(video_buttons_frame, text="Download a Video")
download_video_button.pack(fill='x', pady=5)

update_video_button = tk.Button(video_buttons_frame, text="Update Video", command=lambda: show_frame(update_video_frame))
update_video_button.pack(fill='x', pady=5)

# Navigation buttons at the bottom
video_management_back_button = tk.Button(video_management_frame, text="Back to last page", command=back_to_welcome)
video_management_back_button.pack(side='left', padx=10, pady=20)

video_management_exit_button = tk.Button(video_management_frame, text="Exit System", command=quit_app)
video_management_exit_button.pack(side='right', padx=10, pady=20)



# ----------------------------------------------------------------------User management-------------------------------------------------------------------------------


# User Management frame setup
user_management_frame = tk.Frame(root)
user_management_label = tk.Label(user_management_frame, text="User Management", font=("Arial", 20))
user_management_label.pack(pady=30)

# This frame will contain all the user management buttons
user_buttons_frame = tk.Frame(user_management_frame)
user_buttons_frame.pack(pady=10)

# Add user management buttons here

search_user_by_id_button = tk.Button(user_buttons_frame, text="Search a User by ID", command=lambda: show_frame(search_user_by_id_frame))
search_user_by_id_button.pack(fill='x', pady=5)

search_by_keyword_button = tk.Button(user_buttons_frame, text="Search a User by Keywords", command=lambda: show_frame(search_user_by_keyword_frame))
search_by_keyword_button.pack(fill='x', pady=5)

list_all_users_button = tk.Button(user_buttons_frame, text="List All Users", command=lambda: [show_frame(list_users_frame), populate_users_text_area(client.list_all_users())])
list_all_users_button.pack(fill='x', pady=5)

update_user_information_button = tk.Button(user_buttons_frame, text="Update User Information", command=lambda: show_frame(update_user_frame))
update_user_information_button.pack(fill='x', pady=5)

search_by_keyword_button = tk.Button(user_buttons_frame, text="Cancel a User")
search_by_keyword_button.pack(fill='x', pady=5)

# Navigation buttons at the bottom
user_management_back_button = tk.Button(user_management_frame, text="Back to last page", command=back_to_welcome)
user_management_back_button.pack(side='left', padx=10, pady=20)

user_management_exit_button = tk.Button(user_management_frame, text="Exit System", command=quit_app)
user_management_exit_button.pack(side='right', padx=10, pady=20)

# Modify the manage_users_button command to show_user_management
manage_users_button.config(command=show_user_management)


# ----------------------------------------------------------------------comment management-------------------------------------------------------------------------------


# Comment Management frame setup
comment_management_frame = tk.Frame(root)
comment_management_label = tk.Label(comment_management_frame, text="Comment Management", font=("Arial", 20))
comment_management_label.pack(pady=30)

# This frame will contain all the comment management buttons
comment_buttons_frame = tk.Frame(comment_management_frame)
comment_buttons_frame.pack(pady=10)

# Add comment management buttons here
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

# Navigation buttons at the bottom
comment_management_back_button = tk.Button(comment_management_frame, text="Back to last page", command=back_to_welcome)
comment_management_back_button.pack(side='left', padx=10, pady=20)

comment_management_exit_button = tk.Button(comment_management_frame, text="Exit System", command=quit_app)
comment_management_exit_button.pack(side='right', padx=10, pady=20)

# Modify the manage_comments_button command to show_comment_management
manage_comments_button.config(command=show_comment_management)

# ----------------------------------------------------------------------upload video-------------------------------------------------------------------------------


# Upload Video frame setup
upload_video_frame = tk.Frame(root)
upload_video_label = tk.Label(upload_video_frame, text="Upload a Video", font=("Arial", 20))
upload_video_label.pack(pady=30)

# Entry for the video title
title_label = tk.Label(upload_video_frame, text="Title")
title_label.pack()
title_entry = tk.Entry(upload_video_frame)
title_entry.pack(pady=5)

# Entry for the username
upload_username_label = tk.Label(upload_video_frame, text="Username")
upload_username_label.pack()
upload_username_entry = tk.Entry(upload_video_frame)
upload_username_entry.pack(pady=5)

# Entry for the video file path
video_path_label = tk.Label(upload_video_frame, text="Video File Path")
video_path_label.pack()
video_path_entry = tk.Entry(upload_video_frame)
video_path_entry.pack(pady=5)

# Button to browse for video file
def browse_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    video_path_entry.delete(0, tk.END)
    video_path_entry.insert(0, file_path)

browse_button = tk.Button(upload_video_frame, text="Browse...", command=browse_video_file)
browse_button.pack(pady=5)

# Entry for the video duration
duration_label = tk.Label(upload_video_frame, text="Duration (seconds)")
duration_label.pack()
duration_entry = tk.Entry(upload_video_frame)
duration_entry.pack(pady=5)

# Button to upload the video
def perform_video_upload():
    title = title_entry.get()
    username = upload_username_entry.get()
    video_path = video_path_entry.get()
    duration = duration_entry.get()

    if not title or not username or not video_path or not duration:
        messagebox.showwarning("Warning", "All fields must be filled out to upload.")
        return

    try:
        with open(video_path, 'rb') as video:
            files = {'video': (video_path, video, 'video/mp4')}
            data = {'title': title, 'username': username, 'duration': duration}
            response = requests.post(f"{API_BASE_URL}/upload_video", files=files, data=data)
            if response.status_code == 202:
                messagebox.showinfo("Success", "Video uploaded successfully!")
            else:
                result = response.json()
                messagebox.showerror("Upload Failed", result.get('error', 'Unknown error occurred.'))
    except FileNotFoundError:
        messagebox.showerror("Error", "Video file not found at specified path.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

upload_button = tk.Button(upload_video_frame, text="Upload Video", command=perform_video_upload)
upload_button.pack(pady=10)

# Navigation buttons at the bottom
video_upload_back_button = tk.Button(upload_video_frame, text="Back to Video Management", command=show_video_management)
video_upload_back_button.pack(side='left', padx=10, pady=20)

video_upload_exit_button = tk.Button(upload_video_frame, text="Exit System", command=quit_app)
video_upload_exit_button.pack(side='right', padx=10, pady=20)

# Modify the upload_video_button command in video management frame to show the upload video frame
upload_video_button.config(command=lambda: show_frame(upload_video_frame))

# Function to switch between frames
def show_frame(frame):
    clear_frames()
    frame.pack(fill='both', expand=True)




# ----------------------------------------------------------------------search video by ID-------------------------------------------------------------------------------
# Frame setup for Search Video by ID
search_video_id_frame = tk.Frame(root)
search_video_id_label = tk.Label(search_video_id_frame, text="Search Video by ID", font=("Arial", 20))
search_video_id_label.pack(pady=30)

# Entry for Video ID with input validation for numeric input
video_id_label = tk.Label(search_video_id_frame, text="Video ID")
video_id_label.pack()
video_id_entry = tk.Entry(search_video_id_frame)
video_id_entry.pack(pady=5)

# Label to display real-time input
input_display_label = tk.Label(search_video_id_frame, text="")
input_display_label.pack()

def update_input_display(event):
    current_input = video_id_entry.get()
    if current_input.isdigit():
        input_display_label.config(text=f"Current Input: {current_input}")
    else:
        video_id_entry.delete(0, tk.END)
        messagebox.showerror("Invalid Input", "Please enter a numeric value.")

video_id_entry.bind("<KeyRelease>", update_input_display)

# Listbox for displaying video details
video_details_listbox = tk.Listbox(search_video_id_frame, width=70, height=15)
video_details_listbox.pack(pady=10)

def populate_video_details_listbox(video):
    video_details_listbox.delete(0, tk.END)
    if 'error' in video:
        messagebox.showerror("Error", video['error'])
    else:
        video_details_listbox.insert(tk.END, f"ID: {video['id']}, Title: {video['title']}, Author: {video['author']}")
        video_details_listbox.insert(tk.END, f"Duration: {video['duration_seconds']} seconds")
        video_details_listbox.insert(tk.END, f"Size: {video['size']} bytes")
        video_details_listbox.insert(tk.END, f"Uploaded at: {video['upload_time']}")

def perform_video_id_search():
    video_id = video_id_entry.get()
    try:
        video = client.get_video_details(int(video_id))  # Assuming you convert to integer before calling
        populate_video_details_listbox(video)
    except ValueError:
        messagebox.showerror("Input Error", "Invalid ID format.")
    except Exception as e:
        messagebox.showerror("Search Error", str(e))

search_button = tk.Button(search_video_id_frame, text="Search Video", command=perform_video_id_search)
search_button.pack(pady=10)

back_to_video_management_button = tk.Button(search_video_id_frame, text="Back to Video Management", command=lambda: show_frame("video_management_frame"))
back_to_video_management_button.pack(side='left', padx=10, pady=20)

exit_search_video_id_frame_button = tk.Button(search_video_id_frame, text="Exit System", command=root.quit)
exit_search_video_id_frame_button.pack(side='right', padx=10, pady=20)
search_video_keywords_button.config(command=lambda: show_frame(search_video_id_frame_frame))
# ----------------------------------------------------------------------search video by keywords-------------------------------------------------------------------------------


video_id_label = tk.Label(search_video_id_frame, text="Video ID")
video_id_label.pack()
video_id_entry = tk.Entry(search_video_id_frame)
video_id_entry.pack(pady=5)

# Function to validate and convert the input to numeric
def update_input_display(event):
    current_input = video_id_entry.get()
    if current_input.isdigit():
        input_display_label.config(text=f"Current Input: {current_input}")
    else:
        input_display_label.config(text="Please enter a valid numeric ID")

video_id_entry.bind("<KeyRelease>", update_input_display)

# Function to perform video ID search
def perform_video_id_search():
    video_id = video_id_entry.get()
    try:
        # Convert the video ID to int before performing search
        video_info = client.search_video_by_id(int(video_id))
        populate_video_details_listbox(video_info)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric ID")
    except Exception as e:
        messagebox.showerror("Search Error", str(e))

# Search button for video ID
search_button = tk.Button(search_video_id_frame, text="Search Video", command=perform_video_id_search)
search_button.pack(pady=10)
search_video_id_button.config(command=lambda: show_frame(search_video_frame))


# ----------------------------------------------------------------------list all videos-------------------------------------------------------------------------------


# List All Videos frame setup
list_videos_frame = tk.Frame(root)
list_videos_label = tk.Label(list_videos_frame, text="List of All Videos", font=("Arial", 20))
list_videos_label.pack(pady=30)

# ScrolledText area for displaying all videos
videos_text_area = scrolledtext.ScrolledText(list_videos_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
videos_text_area.pack(pady=10)

# Function to populate the text area with video details
def populate_videos_text_area(videos):
    videos_text_area.config(state='normal')
    videos_text_area.delete('1.0', tk.END)
    if 'error' in videos:
        messagebox.showerror("Error", videos['error'])
    else:
        for video in videos:
            videos_text_area.insert(tk.END, f"ID: {video['id']}, Title: {video['title']}, Author: {video['author']}\n")
            videos_text_area.insert(tk.END, f"Path: {video['video_path']}, Size: {video['bytes']} bytes\n")
            videos_text_area.insert(tk.END, f"Duration: {video['duration_seconds']} seconds, Uploaded at: {video['upload_time']}\n")
            videos_text_area.insert(tk.END, "-" * 80 + "\n")  # Separator for readability
    videos_text_area.config(state='disabled')

# Function to fetch and display all videos
def show_all_videos():
    try:
        videos = client.list_all_videos()
        populate_videos_text_area(videos)
    except Exception as e:
        messagebox.showerror("List Error", str(e))

# Button to refresh and list all videos
refresh_button = tk.Button(list_videos_frame, text="Refresh List", command=show_all_videos)
refresh_button.pack(pady=10)

# Back button to return to the video management page
back_to_video_management_button = tk.Button(list_videos_frame, text="Back to Video Management", command=show_video_management)
back_to_video_management_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_list_videos_frame_button = tk.Button(list_videos_frame, text="Exit System", command=quit_app)
exit_list_videos_frame_button.pack(side='right', padx=10, pady=20)

# Modify the list_videos_button command in video management frame to show the list videos frame and automatically populate the list
list_videos_button.config(command=lambda: [show_frame(list_videos_frame), show_all_videos()])





# ----------------------------------------------------------------------download by ID-------------------------------------------------------------------------------



# Download Video frame setup
download_video_frame = tk.Frame(root)
download_video_label = tk.Label(download_video_frame, text="Download a Video by ID", font=("Arial", 20))
download_video_label.pack(pady=30)

# Entry for the video ID
video_id_label = tk.Label(download_video_frame, text="Video ID")
video_id_label.pack()
video_id_entry = tk.Entry(download_video_frame)
video_id_entry.pack(pady=5)

# Function to initiate the download
def initiate_download():
    video_id = video_id_entry.get().strip()  # Strip to remove any leading/trailing whitespace
    download_folder = filedialog.askdirectory()

    # Check if the download folder was selected
    if not download_folder:
        messagebox.showerror("Error", "Please choose a download folder.")
        return

    # Check if the video ID is a valid integer
    try:
        int(video_id)  # Attempt to convert to integer to validate
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric video ID.")
        return

    # If all checks pass, proceed with download
    message = client.download_video_by_id(video_id, download_folder)
    messagebox.showinfo("Download", message)


# Button to start the download
download_button = tk.Button(download_video_frame, text="Download Video", command=initiate_download)
download_button.pack(pady=10)

# Back button to return to the video management page
back_to_video_management_button = tk.Button(download_video_frame, text="Back to Video Management", command=show_video_management)
back_to_video_management_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_download_frame_button = tk.Button(download_video_frame, text="Exit System", command=quit_app)
exit_download_frame_button.pack(side='right', padx=10, pady=20)

# Modify the download_video_button command in video management frame to show the download video frame
download_video_button.config(command=lambda: show_frame(download_video_frame))





# ----------------------------------------------------------------------Update Video Info-------------------------------------------------------------------------------


# Function to call the update_video_title from client module
def update_video():
    video_id = video_id_entry.get().strip()
    new_title = new_title_entry.get().strip()
    if not video_id or not new_title:
        messagebox.showerror("Error", "Both video ID and new title are required.")
        return

    try:
        int(video_id)  # Check if video_id is an integer
    except ValueError:
        messagebox.showerror("Error", "Video ID must be a numeric integer.")
        return

    result = client.update_video_title(video_id, new_title)
    if result and 'error' in result:
        messagebox.showerror("Update Failed", result['error'])
    elif result:
        messagebox.showinfo("Success", "Video title updated successfully!")
    else:
        messagebox.showerror("Update Failed", "No response received from server.")

# Setup for Update Video Frame
update_video_frame = tk.Frame(root)
update_video_label = tk.Label(update_video_frame, text="Update Video Information", font=("Arial", 20))
update_video_label.pack(pady=20)

# Entry for Video ID
video_id_label = tk.Label(update_video_frame, text="Video ID:")
video_id_label.pack()
video_id_entry = tk.Entry(update_video_frame)
video_id_entry.pack(pady=5)

# Entry for New Title
new_title_label = tk.Label(update_video_frame, text="New Title:")
new_title_label.pack()
new_title_entry = tk.Entry(update_video_frame)
new_title_entry.pack(pady=5)

# Button to submit the update
update_button = tk.Button(update_video_frame, text="Update Video", command=update_video)
update_button.pack(pady=20)

# Back button to video management
back_button = tk.Button(update_video_frame, text="Back to Video Management", command=lambda: show_frame(video_management_frame))
back_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_button = tk.Button(update_video_frame, text="Exit System", command=root.quit)
exit_button.pack(side='right', padx=10, pady=20)




# ----------------------------------------------------------------------delete a video-------------------------------------------------------------------------------





# Function to delete a video
def delete_video():
    video_id = video_id_entry.get().strip()
    if not video_id:
        messagebox.showerror("Error", "Video ID is required.")
        return

    try:
        int(video_id)  # Check if video_id is an integer
    except ValueError:
        messagebox.showerror("Error", "Video ID must be a numeric integer.")
        return

    result = client.delete_video(video_id)  # Call to client function to delete video
    if 'error' in result:
        messagebox.showerror("Deletion Failed", result['error'])
    else:
        messagebox.showinfo("Success", "Video deleted successfully from OSS and SQL database.")

# Setup for Delete Video Frame
delete_video_frame = tk.Frame(root)
delete_video_label = tk.Label(delete_video_frame, text="Delete Video by ID", font=("Arial", 20))
delete_video_label.pack(pady=20)

video_id_label = tk.Label(delete_video_frame, text="Video ID:")
video_id_label.pack()
video_id_entry = tk.Entry(delete_video_frame)
video_id_entry.pack(pady=5)

delete_button = tk.Button(delete_video_frame, text="Delete Video", command=delete_video)
delete_button.pack(pady=20)

back_button = tk.Button(delete_video_frame, text="Back to Video Management", command=lambda: show_frame(video_management_frame))
back_button.pack(side='left', padx=10, pady=20)

exit_button = tk.Button(delete_video_frame, text="Exit System", command=root.quit)
exit_button.pack(side='right', padx=10, pady=20)

# Adding the delete video button to video management frame
delete_video_button = tk.Button(video_buttons_frame, text="Delete Video", command=lambda: show_frame(delete_video_frame))
delete_video_button.pack(fill='x', pady=5)



# ----------------------------------------------------------------------Search a user by ID-------------------------------------------------------------------------------



# Search User by ID frame setup
search_user_by_id_frame = tk.Frame(root)
search_user_by_id_label = tk.Label(search_user_by_id_frame, text="Search a User by ID", font=("Arial", 20))
search_user_by_id_label.pack(pady=30)

# Entry for the user ID
user_id_label = tk.Label(search_user_by_id_frame, text="User ID:")
user_id_label.pack()
user_id_entry = tk.Entry(search_user_by_id_frame)
user_id_entry.pack(pady=5)

# Text area for displaying user details
user_details_text = scrolledtext.ScrolledText(search_user_by_id_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
user_details_text.pack(pady=10)

# Function to display user details
def display_user_details(user_info):
    user_details_text.config(state='normal')
    user_details_text.delete('1.0', tk.END)
    if 'error' in user_info:
        messagebox.showerror("Error", user_info['error'])
    else:
        user_details_text.insert('1.0', f"User ID: {user_info['id']}\nUsername: {user_info['username']}\n")
        user_details_text.insert(tk.END, "\nComments:\n")
        for comment in user_info['comments']:
            user_details_text.insert(tk.END, f"  - {comment['text']} (Video ID {comment['video_id']})\n")
        user_details_text.insert(tk.END, "\nVideos:\n")
        for video in user_info['videos']:
            user_details_text.insert(tk.END, f"  - {video['title']} (Video ID {video['id']})\n")
    user_details_text.config(state='disabled')

# Button to search for the user
def perform_user_search():
    user_id = user_id_entry.get()
    if not user_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric user ID.")
        return
    try:
        user_info = client.get_user_info(user_id)
        display_user_details(user_info)
    except requests.exceptions.HTTPError as http_err:
        # Check if the exception is a 404 Not Found error
        if http_err.response.status_code == 404:
            messagebox.showerror("Search Error", "User with the provided ID not found.")
        else:
            messagebox.showerror("Search Error", f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Search Error", f"An error occurred: {err}")
    except Exception as e:
        messagebox.showerror("Search Error", f"An unexpected error occurred: {e}")



search_user_button = tk.Button(search_user_by_id_frame, text="Search User", command=perform_user_search)
search_user_button.pack(pady=10)

# Back button to return to the user management page
back_to_user_management_button = tk.Button(search_user_by_id_frame, text="Back to User Management", command=show_user_management)
back_to_user_management_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_search_user_frame_button = tk.Button(search_user_by_id_frame, text="Exit System", command=quit_app)
exit_search_user_frame_button.pack(side='right', padx=10, pady=20)




# ----------------------------------------------------------------------search a user by keyword-------------------------------------------------------------------------------





# Search User by Keyword frame setup
search_user_by_keyword_frame = tk.Frame(root)
search_user_by_keyword_label = tk.Label(search_user_by_keyword_frame, text="Search Users by Keyword", font=("Arial", 20))
search_user_by_keyword_label.pack(pady=30)

# Entry for the username keyword
username_keyword_label = tk.Label(search_user_by_keyword_frame, text="Keyword:")
username_keyword_label.pack()
username_keyword_entry = tk.Entry(search_user_by_keyword_frame)
username_keyword_entry.pack(pady=5)

# Listbox for displaying users
users_listbox = tk.Listbox(search_user_by_keyword_frame, width=70, height=15)
users_listbox.pack(pady=10)

# Function to populate the listbox with user details
def populate_users_listbox(users):
    users_listbox.delete(0, tk.END)
    for user in users:
        user_entry = f"User ID: {user['id']}, Username: {user['username']}"
        users_listbox.insert(tk.END, user_entry)
        for comment in user['comments']:
            comment_entry = f"    Comment: {comment['text']} (Created At: {comment['created_at']})"
            users_listbox.insert(tk.END, comment_entry)
        for video in user['videos']:
            video_entry = f"    Video: {video['title']} (Size: {video['size']} bytes, Uploaded At: {video['upload_time']})"
            users_listbox.insert(tk.END, video_entry)
        users_listbox.insert(tk.END, '-'*80)  # Separator for readability

# Button to search for the users
def perform_user_keyword_search():
    username_keyword = username_keyword_entry.get().strip()
    if not username_keyword:
        messagebox.showerror("Error", "Please enter a keyword to search.")
        return
    try:
        user_details_list = client.search_users(username_keyword)
        if 'error' in user_details_list:
            messagebox.showerror("Search Error", user_details_list['error'])
        else:
            populate_users_listbox(user_details_list)
    except Exception as e:
        messagebox.showerror("Search Error", str(e))

search_user_button = tk.Button(search_user_by_keyword_frame, text="Search Users", command=perform_user_keyword_search)
search_user_button.pack(pady=10)

# Back button to return to the user management page
back_to_user_management_button = tk.Button(search_user_by_keyword_frame, text="Back to User Management", command=show_user_management)
back_to_user_management_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_search_user_by_keyword_frame_button = tk.Button(search_user_by_keyword_frame, text="Exit System", command=quit_app)
exit_search_user_by_keyword_frame_button.pack(side='right', padx=10, pady=20)



# ----------------------------------------------------------------------list all users-------------------------------------------------------------------------------



# List All Users frame setup
list_users_frame = tk.Frame(root)
list_users_label = tk.Label(list_users_frame, text="List of All Users", font=("Arial", 20))
list_users_label.pack(pady=30)

# ScrolledText area for displaying all users
users_text_area = scrolledtext.ScrolledText(list_users_frame, width=70, height=15, wrap=tk.WORD, state='disabled')
users_text_area.pack(pady=10)

# Function to populate the text area with user details
def populate_users_text_area(users):
    users_text_area.config(state='normal')
    users_text_area.delete('1.0', tk.END)
    if 'error' in users:
        messagebox.showerror("Error", users['error'])
    else:
        for user in users:
            users_text_area.insert(tk.END, f"ID: {user['id']}, Username: {user['username']}\n")
            users_text_area.insert(tk.END, "Comments:\n")
            for comment in user['comments']:
                users_text_area.insert(tk.END, f"  - {comment['text']} (Comment ID {comment['id']})\n")
            users_text_area.insert(tk.END, "Videos:\n")
            for video in user['videos']:
                users_text_area.insert(tk.END, f"  - {video['title']} (Video ID {video['id']})\n")
            users_text_area.insert(tk.END, "-" * 80 + "\n")  # Separator for readability
    users_text_area.config(state='disabled')

# Button to refresh and list all users
refresh_users_button = tk.Button(list_users_frame, text="Refresh List", command=lambda: populate_users_text_area(client.list_all_users()))
refresh_users_button.pack(pady=10)

# Back button to return to the user management page
back_to_user_management_button = tk.Button(list_users_frame, text="Back to User Management", command=show_user_management)
back_to_user_management_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_list_users_frame_button = tk.Button(list_users_frame, text="Exit System", command=quit_app)
exit_list_users_frame_button.pack(side='right', padx=10, pady=20)



# ----------------------------------------------------------------------update user info-------------------------------------------------------------------------------




# Update User Information frame setup
update_user_frame = tk.Frame(root)
update_user_label = tk.Label(update_user_frame, text="Update User Information", font=("Arial", 20))
update_user_label.pack(pady=20)

# Entry for User ID
user_id_label = tk.Label(update_user_frame, text="User ID:")
user_id_label.pack()
user_id_entry = tk.Entry(update_user_frame)
user_id_entry.pack(pady=5)

# Entry for New Username
new_username_label = tk.Label(update_user_frame, text="New Username:")
new_username_label.pack()
new_username_entry = tk.Entry(update_user_frame)
new_username_entry.pack(pady=5)

# Entry for New Password
new_password_label = tk.Label(update_user_frame, text="New Password:")
new_password_label.pack()
new_password_entry = tk.Entry(update_user_frame, show="*")
new_password_entry.pack(pady=5)


# Function to call the update_user_info function and handle response
# 函数用来提交更新并处理响应
def submit_update():
    user_id = user_id_entry.get().strip()
    new_username = new_username_entry.get().strip()
    new_password = new_password_entry.get().strip()

    if not user_id.isdigit():
        messagebox.showerror("Error", "ID must be a numerical value")
        return

    result = client.update_user_info(user_id, new_username, new_password)
    if 'error' in result:
        messagebox.showerror("Failed", result['error'])
    else:
        messagebox.showinfo("Successful", "Updated successfully!")




# Button to submit the update
update_button = tk.Button(update_user_frame, text="Update User", command=submit_update)
update_button.pack(pady=20)

# Back button to user management
back_button = tk.Button(update_user_frame, text="Back to User Management", command=show_user_management)
back_button.pack(side='left', padx=10, pady=20)

# Exit button to exit the system
exit_button = tk.Button(update_user_frame, text="Exit System", command=quit_app)
exit_button.pack(side='right', padx=10, pady=20)



# ----------------------------------------------------------------------show login-------------------------------------------------------------------------------
def print_focus():
    focused_widget = root.focus_get()
    if focused_widget:
        print(f"当前焦点控件: {focused_widget}")
    else:
        print("当前没有控件拥有焦点")
    root.after(1000, print_focus)  # 每1000毫秒（1秒）执行一次



show_login()
print_focus()  # 开始监视焦点
root.mainloop()
