
import requests
from requests.sessions import Session

import os
from flask import Flask, request, jsonify


API_BASE_URL = 'http://127.0.0.1:5000'

session = Session()
current_user = None

def create_user(username, password):
    response = requests.post(f"{API_BASE_URL}/create_user", json={'username': username, 'password': password})
    if response.status_code == 201:
        try:
            response_data = response.json()
            if 'error' in response_data:
                print(f"Error: {response_data['error']}")
                return False
            else:
                print("User created successfully.")
                return True
        except ValueError:
            print("Response is not in JSON format:", response.text)
            return False
    else:
        print(f"Failed to create user, status code: {response.status_code}")
        return False



def upload_video(title, username, video_path, duration):
    try:
        with open(video_path, 'rb') as video:
            files = {'video': video}
            data = {'title': title, 'username': username, 'duration': duration}
            response = requests.post(f"{API_BASE_URL}/upload_video", files=files, data=data)
            print(response.json())
    except FileNotFoundError:
        print("Video file not found at specified path")
    except Exception as e:
        print(f"An error occurred: {e}")


# User log in
def login(username, password):
    global current_user
    response = session.post(f"{API_BASE_URL}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        try:
            response_data = response.json()
            if 'error' in response_data:
                print(f"Login failed: {response_data['error']}")
                return False
            else:
                current_user = username  # Set current user globally on successful login
                print("Login successful!")
                return True
        except ValueError:
            print("Response is not in JSON format:", response.text)
            return False
    else:
        print(f"Failed to connect to server, status code: {response.status_code}")
        return False


def post_comment(video_id, user_id, comment_text):
    data = {
        'video_id': video_id,
        'user_id': user_id,
        'comment_text': comment_text
    }
    response = requests.post(f"{API_BASE_URL}/post_comment", json=data)
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format:", response.text)


def download_video_by_id(video_id, download_folder):
    params = {'id': video_id}
    response = requests.get(f"{API_BASE_URL}/download_video", params=params)

    try:
        video_info = response.json()
        if 'url' in video_info:
            video_url = video_info['url']
            local_filename = os.path.join(download_folder, f"{video_id}.mp4")
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return f"Video downloaded successfully as {local_filename}"
        else:
            return video_info.get('error', 'An unexpected error occurred')
    except Exception as e:
        return str(e)



def get_user_info(user_id):
    response = requests.get(f"{API_BASE_URL}/user_info", params={'user_id': user_id})
    if response.status_code == 200:
        return response.json()  # Return the parsed JSON data
    else:
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code


def delete_user(user_id):
    response = requests.post(f"{API_BASE_URL}/delete_user", json={'user_id': user_id})
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format:", response.text)


def delete_comment(comment_id):
    response = requests.post(f"{API_BASE_URL}/delete_comment", json={'comment_id': comment_id})
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format:", response.text)



def list_all_users():
    response = requests.get(f"{API_BASE_URL}/list_all_users")
    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        return {"error": "Failed to retrieve the list of users"}


def list_all_videos():
    response = requests.get(f"{API_BASE_URL}/list_all_videos")
    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        return {"error": "Failed to retrieve the list of videos"}



def list_all_comments():
    response = requests.get(f"{API_BASE_URL}/list_all_comments")
    try:
        comments = response.json()
        for comment in comments:
            print(f"Comment ID: {comment['id']}, Video ID: {comment['video_id']}, User ID: {comment['user_id']}")
            print(f"Comment: {comment['comment_text']}, Created at: {comment['created_at']}")
            print("-" * 40)  # Separator for readability
    except ValueError:
        print("Response is not in JSON format:", response.text)


def get_video_details(video_id):
    response = requests.get(f"{API_BASE_URL}/video_details", params={'video_id': video_id})
    if response.status_code == 200:
        return response.json()  # Success
    elif response.status_code == 404:
        return {"error": "Video not found"}  # Not found error
    else:
        response.raise_for_status()  # Raises an HTTPError for other unsuccessful status codes




def get_comment_details(comment_id):
    response = requests.get(f"{API_BASE_URL}/comment_details", params={'comment_id': comment_id})
    try:
        comment_details = response.json()
        if 'error' not in comment_details:
            print(f"Comment ID: {comment_details['id']}")
            print(f"Video ID: {comment_details['video_id']}")
            print(f"User ID: {comment_details['user_id']}")
            print(f"Username: {comment_details['username']}")
            print(f"Comment Text: {comment_details['comment_text']}")
            print(f"Created At: {comment_details['created_at']}")
        else:
            print(comment_details['error'])
    except ValueError:
        print("Response is not in JSON format:", response.text)


def update_video_title(video_id, new_title):
    data = {
        'video_id': video_id,
        'new_title': new_title
    }
    response = requests.post(f"{API_BASE_URL}/update_video_title", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        try:
            return response.json()
        except ValueError:
            return {'error': 'Failed to parse response, status code: ' + str(response.status_code)}


def update_comment(comment_id, new_content):
    data = {
        'comment_id': comment_id,
        'new_content': new_content
    }
    response = requests.post(f"{API_BASE_URL}/update_comment", json=data)
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format:", response.text)


def search_users(username_keyword):
    response = requests.get(f"{API_BASE_URL}/search_users", params={'username_keyword': username_keyword})
    if response.status_code == 200:
        return response.json()  # Return the parsed JSON data
    else:
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code


def search_videos(keyword):
    response = requests.get(f"{API_BASE_URL}/search_videos", params={'keyword': keyword})
    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        return {"error": "Failed to retrieve videos"}


def search_comments(keyword):
    response = requests.get(f"{API_BASE_URL}/search_comments", params={'keyword': keyword})
    try:
        comments = response.json()
        if 'error' not in comments:
            for comment in comments:
                print(f"Comment ID: {comment['comment_id']}, Text: {comment['text']}")
                print(f"Created At: {comment['created_at']}, Video Title: {comment['video_title']}")
                print(f"Commenter ID: {comment['commenter_id']}, Commenter Username: {comment['commenter_username']}")
                print("\n")
        else:
            print(comments['error'])
    except ValueError:
        print("Response is not in JSON format:", response.text)

# Delete a video by ID
def delete_video(video_id):
    url = f"{API_BASE_URL}/delete_video"
    data = {'video_id': video_id}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()  # 确保即使是成功的消息也是以JSON形式返回
        else:
            return response.json()  # 返回错误信息的JSON
    except ValueError:
        # 当返回不是JSON格式时
        return {'error': "Failed to parse response as JSON."}
    except Exception as e:
        # 处理其他异常，如网络问题等
        return {'error': str(e)}


def update_user_info(user_id, new_username, new_password):
    try:
        user_id = int(user_id)
    except ValueError:
        return {"error": "User ID must be an integer"}

    data = {
        'user_id': user_id,
        'new_username': new_username,
        'new_password': new_password
    }
    response = requests.post(f"{API_BASE_URL}/update_user_info", json=data)
    if response.status_code == 200:
        return response.json()  # 如果状态码为200，返回响应中的JSON数据
    else:
        return {"error": response.text}  # 如果状态码不是200，返回响应文本中的错误信息




def main():
    logged_in = False
    while True:
        if not logged_in:
            print("\nMenu:")
            print("1. Create a new user")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                create_user(username, password)
            elif choice == '2':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                logged_in = login(username, password)
                if logged_in:
                    print("Login successful!")
                else:
                    print("Invalid username or password.")
            elif choice == '3':
                break
        else:
            print("\nMenu:")
            print("2. Upload a video")
            print("3. Post a comment")
            print("4. Down a video by title")
            print("5. Search a user information by ID")
            print("6. Cancel a user by ID")
            print("7. Delete a comment by ID")
            print("8. List all users")
            print("9. List all videos")
            print("10. List all comments")
            print("11. Search a video by ID")
            print("12. Search a comment by ID")
            print("13. Update video information")
            print("14. Update comment information")
            print("15. Search a user by a key word in username")
            print("16. Search a video by a key word")
            print("17. Search a comment by a key word")
            print("18. Delete a video by ID")
            print("19. Return to login")
            print("20. Exit")
            choice = input("Enter your choice: ")

            if choice == '2':
                title = input("Enter video title: ")
                username = input("Input your username: ")
                video_path = input("Enter the path to the video file: ")
                duration = input("Enter the video duration in seconds: ")
                upload_video(title, username, video_path, duration)
            elif choice == '3':
                video_id = input("Enter the video ID to comment on: ")
                user_id = input("Enter your user ID: ")
                comment_text = input("Enter your comment: ")
                post_comment(video_id, user_id, comment_text)
            elif choice == '4':
                video_title = input("Enter the title of video you want to download: ")
                download_video_by_title(video_title)
            elif choice == '5':
                user_id = input("Enter the user ID you want to search: ")
                get_user_info(user_id)
            elif choice == '6':
                user_id = input("Enter the user ID to delete: ")
                delete_user(user_id)
            elif choice == '7':
                comment_id = input("Enter the comment ID to delete: ")
                delete_comment(comment_id)
            elif choice == '8':
                list_all_users()
            elif choice == '9':
                list_all_videos()
            elif choice == '10':
                list_all_comments()
            elif choice == '11':
                video_id = input("Enter the video ID to get details: ")
                get_video_details(video_id)
            elif choice == '12':
                comment_id = input("Enter the comment ID to get details: ")
                get_comment_details(comment_id)
            elif choice == '13':
                video_id = input("Enter the video ID for the title update: ")
                new_title = input("Enter the new title for the video: ")
                update_video_title(video_id, new_title)
            elif choice == '14':
                comment_id = input("Enter the comment ID for the content update: ")
                new_content = input("Enter the new content for the comment: ")
                update_comment(comment_id, new_content)
            elif choice == '15':
                username_keyword = input("Enter the username keyword to search: ")
                search_users(username_keyword)
            elif choice == '16':
                keyword = input("Enter the keyword to search in video titles: ")
                search_videos(keyword)
            elif choice == '17':
                keyword = input("Enter the keyword to search comments: ")
                search_comments(keyword)
            elif choice == '18':
                video_id = input("Enter the video ID to delete: ")
                delete_video(video_id)
            elif choice == '19':
                logged_in = False
            elif choice == '20':
                import sys
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
