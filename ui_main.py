import tkinter as tk
from controllers import show_frame, back_to_welcome, quit_app
from ui_login import setup_login_frame
from ui_welcome import setup_welcome_frame

from ui_video_management import setup_video_management_frame
from ui_user_management import setup_user_management_frame
from ui_comment_management import setup_comment_management_frame
from ui_upload_video import setup_upload_video_frame
from ui_search_video_by_ID import setup_search_video_by_ID_frame
from ui_search_video_by_keywords import setup_search_video_by_keywords_frame
from ui_list_all_videos import setup_list_videos_frame
from ui_download_video_frame import setup_download_video_frame
from ui_update_video import setup_update_video_frame
from ui_delete_video import setup_delete_video_frame

from ui_search_user_by_id import setup_search_user_by_id_frame
from ui_search_user_by_keywords import setup_search_user_by_keywords_frame
from ui_list_all_users import setup_list_all_users_frame
from ui_update_user import setup_update_user_frame
from ui_delete_user import setup_delete_user_frame

from ui_post_comment import setup_post_comment_frame
from ui_find_comment_by_id import setup_find_comment_by_id_frame
from ui_find_comment_by_keyword import setup_find_comment_by_keyword_frame
from ui_list_all_comments import setup_list_all_comments_frame
from ui_update_comment import setup_update_comment_frame
from ui_delete_comment import setup_delete_comment_frame





def main():
    root = tk.Tk()
    root.title("Video Management System")
    root.geometry('800x600')

    # Initialize and attach frames to root
    root.login_frame = tk.Frame(root)
    root.welcome_frame = tk.Frame(root)

    root.video_management_frame = tk.Frame(root)
    root.user_management_frame = tk.Frame(root)
    root.comment_management_frame = tk.Frame(root)

    root.upload_video_frame = tk.Frame(root)  # Assuming this is also initialized
    root.search_video_by_ID_frame = tk.Frame(root)
    root.search_video_by_keywords_frame = tk.Frame(root)
    root.list_videos_frame = tk.Frame(root)
    root.download_video_frame=tk.Frame(root)
    root.update_video_frame=tk.Frame(root)
    root.delete_video_frame = tk.Frame(root)  # Initialization should happen only once
    setup_delete_video_frame(root, root.delete_video_frame)  # Correct setup call

    root.search_user_by_id_frame = tk.Frame(root)
    setup_search_user_by_id_frame(root, root.search_user_by_id_frame)
    root.search_user_by_keywords_frame = tk.Frame(root)
    setup_search_user_by_keywords_frame(root, root.search_user_by_keywords_frame)
    root.list_all_users_frame = tk.Frame(root)
    setup_list_all_users_frame(root, root.list_all_users_frame)
    root.update_user_frame = tk.Frame(root)
    setup_update_user_frame(root, root.update_user_frame)
    root.delete_user_frame = tk.Frame(root)
    setup_delete_user_frame(root, root.delete_user_frame)

    setup_login_frame(root, root.login_frame, root.welcome_frame)  # Pass welcome_frame as well
    setup_welcome_frame(root, root.welcome_frame)

    setup_video_management_frame(root, root.video_management_frame)
    setup_user_management_frame(root, root.user_management_frame)
    setup_comment_management_frame(root, root.comment_management_frame)

    setup_upload_video_frame(root, root.upload_video_frame)  # Assuming you have a similar setup function
    setup_search_video_by_ID_frame(root, root.search_video_by_ID_frame)
    setup_search_video_by_keywords_frame(root, root.search_video_by_keywords_frame)
    setup_list_videos_frame(root, root.list_videos_frame)
    setup_download_video_frame(root, root.download_video_frame)
    setup_update_video_frame(root, root.update_video_frame)
    setup_delete_video_frame(root, root.delete_video_frame)

    setup_search_user_by_id_frame(root, root.search_user_by_id_frame)
    setup_search_user_by_keywords_frame(root, root.search_user_by_keywords_frame)
    setup_list_all_users_frame(root, root.list_all_users_frame)
    setup_update_user_frame(root, root.update_user_frame)
    setup_delete_user_frame(root, root.delete_user_frame)

    root.post_comment_frame = tk.Frame(root)
    setup_post_comment_frame(root, root.post_comment_frame)
    root.find_comment_by_id_frame = tk.Frame(root)
    setup_find_comment_by_id_frame(root, root.find_comment_by_id_frame)
    root.find_comment_by_keyword_frame = tk.Frame(root)
    setup_find_comment_by_keyword_frame(root, root.find_comment_by_keyword_frame)
    root.list_all_comments_frame = tk.Frame(root)
    setup_list_all_comments_frame(root, root.list_all_comments_frame)
    root.update_comment_frame = tk.Frame(root)
    setup_update_comment_frame(root, root.update_comment_frame)
    root.delete_comment_frame = tk.Frame(root)
    setup_delete_comment_frame(root, root.delete_comment_frame)


    show_frame(root, 'login_frame')

    root.mainloop()


if __name__ == "__main__":
    main()

