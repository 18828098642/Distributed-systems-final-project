from flask import Flask, request, jsonify
import psycopg2
import oss2
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from datetime import datetime
from threading import Thread
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
import psycopg2
import os
from threading import Thread
from datetime import datetime
import os
import tempfile
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, session

app = Flask(__name__)
CORS(app)


# ------------------------------------------------DATABASE AND CLOUD SETUP--------------------------------------------------------------------

# OSS Configuration
access_key_id = 'LTAI5t7bnDvfxGCirU9pT1k3'
access_key_secret = 'aB5jwBhQopvWYqzyBM6kq60deT1ApH'
bucket_name = 'lutproject'
endpoint = 'oss-cn-beijing.aliyuncs.com'

# PostgreSQL connection configuration
pg_username = 'zzx'
pg_password = 'zzx123456#'
pg_hostname = 'pgm-bp1r98h0p4yy51wn3o.pg.rds.aliyuncs.com'
pg_database = 'postgres'

DATABASE_URL = f'postgresql://{pg_username}:{pg_password}@{pg_hostname}:{5432}/{pg_database}'

# OSS initialization
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# Create database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ------------------------------------------------USER--------------------------------------------------------------------


# Route to create user
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username or password is empty
    if not username or not password:
        return jsonify({'error': 'Username and password must not be empty'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;', (username, password))
            user_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201


# User log in
def verify_credentials(username, password):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT password FROM users WHERE username = %s;', (username,))
            user = cur.fetchone()
            if user:
                stored_password = user[0]
                return stored_password == password
            return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(verify_credentials, username, password)
        is_verified = future.result()

    if is_verified:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401



# Check a user info by his/her user id
def fetch_user_details(user_id):
    user_data = {}
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Query to fetch user details
            cur.execute('SELECT id, username FROM users WHERE id = %s;', (user_id,))
            user = cur.fetchone()
            if user:
                user_data['id'] = user[0]
                user_data['username'] = user[1]
                # Query to fetch comments made by the user
                cur.execute('SELECT id, video_id, comment_text, created_at FROM comments WHERE user_id = %s;',
                            (user_id,))
                user_data['comments'] = [
                    {'id': comment[0], 'video_id': comment[1], 'text': comment[2], 'created_at': comment[3].isoformat()}
                    for comment in cur.fetchall()]
                # Query to fetch videos uploaded by the user
                cur.execute(
                    'SELECT id, title, video_path, bytes, duration_seconds, upload_time FROM videos WHERE author = %s;',
                    (user_data['username'],))
                user_data['videos'] = [{'id': video[0], 'title': video[1], 'video_path': video[2], 'size': video[3],
                                        'duration_seconds': video[4], 'upload_time': video[5].isoformat()} for video in
                                       cur.fetchall()]
            else:
                user_data['error'] = 'User not found'
    return user_data

@app.route('/user_info', methods=['GET'])
def user_info():
    user_id = request.args.get('user_id')
    # Validate user_id to ensure it is a valid integer
    try:
        user_id = int(user_id)  # Convert user_id to an integer
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid user ID. User ID must be an integer.'}), 400

    # Using ThreadPoolExecutor to fetch user details in a thread
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_user_details, user_id)
        user_data = future.result()

    if 'error' in user_data:
        return jsonify({'error': user_data['error']}), 404
    else:
        return jsonify(user_data)


# Soft deletion of a user
def soft_delete_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Update the username to indicate the user has been deactivated
            cur.execute('UPDATE users SET username = %s WHERE id = %s RETURNING id;', ('deleted', user_id))
            result = cur.fetchone()
            if result:
                conn.commit()
                return {'message': 'User has been deactivated', 'user_id': result[0]}
            else:
                return {'error': 'User not found'}

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.json.get('user_id')
    # Validate user_id to ensure it is a valid integer
    try:
        user_id = int(user_id)  # Convert user_id to an integer
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid user ID. User ID must be an integer.'}), 400

    # Using ThreadPoolExecutor to perform the soft deletion in a separate thread
    with ThreadPoolExecutor() as executor:
        future = executor.submit(soft_delete_user, user_id)
        result = future.result()

    if 'error' in result:
        return jsonify({'error': result['error']}), 404
    else:
        return jsonify(result)


# List all users
def fetch_all_users_data():
    user_data_list = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Fetch all users
            cur.execute('SELECT id, username FROM users;')
            users = cur.fetchall()

            for user in users:
                user_id, username = user
                user_data = {
                    'id': user_id,
                    'username': username,
                    'comments': [],
                    'videos': []
                }

                # Fetch comments made by the user
                cur.execute('SELECT id, video_id, comment_text, created_at FROM comments WHERE user_id = %s;', (user_id,))
                user_data['comments'] = [
                    {'id': com[0], 'video_id': com[1], 'text': com[2], 'created_at': com[3].isoformat()}
                    for com in cur.fetchall()
                ]

                # Fetch videos posted by the user
                cur.execute('SELECT id, title, video_path, bytes, duration_seconds, upload_time FROM videos WHERE author = %s;', (username,))
                user_data['videos'] = [
                    {'id': vid[0], 'title': vid[1], 'video_path': vid[2], 'size': vid[3], 'duration_seconds': vid[4], 'upload_time': vid[5].isoformat()}
                    for vid in cur.fetchall()
                ]

                user_data_list.append(user_data)

    return user_data_list

@app.route('/list_all_users', methods=['GET'])
def list_all_users():
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_all_users_data)
        user_data_list = future.result()  # 正确地获取函数的返回值
    return jsonify(user_data_list), 200


# Update user info
def update_username_password(user_id, new_username, new_password):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Update username and password in users table
            cur.execute(
                'UPDATE users SET username = %s, password = %s WHERE id = %s;',
                (new_username, new_password, user_id)
            )
            conn.commit()
            # You would need additional queries here to update the username in other tables where it is used as a foreign key.

@app.route('/update_user_info', methods=['POST'])  # 修正路由以匹配客户端请求
def update_user_info():
    data = request.get_json()  # 使用get_json()来获取请求体中的JSON数据
    user_id = data.get('user_id')
    new_username = data.get('new_username')
    new_password = data.get('new_password')  # 在实际应用中，密码应该先进行加密处理

    if not user_id or not new_username or not new_password:
        return jsonify({'error': 'lack user_id, new_username or new_password'}), 400

    update_username_password(user_id, new_username, new_password)  # 直接调用函数执行更新操作
    return jsonify({'message': 'successful'}), 200  # 修改成功状态码应该是200，而不是202


# Search user by username
def fetch_user_details_by_keyword(username_keyword):
    user_details_list = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Search users by username keyword
            cur.execute(
                "SELECT id, username FROM users WHERE username LIKE %s;",
                ('%' + username_keyword + '%',)
            )
            users = cur.fetchall()

            for user_id, username in users:
                # User basic details
                user_details = {
                    'id': user_id,
                    'username': username,
                    'comments': [],
                    'videos': []
                }

                # Fetch comments by user
                cur.execute(
                    "SELECT id, comment_text, created_at FROM comments WHERE user_id = %s;",
                    (user_id,)
                )
                comments = cur.fetchall()
                for comment in comments:
                    user_details['comments'].append({
                        'id': comment[0],
                        'text': comment[1],
                        'created_at': comment[2].isoformat()
                    })

                # Fetch videos by user
                cur.execute(
                    "SELECT id, title, bytes, upload_time FROM videos WHERE author = %s;",
                    (username,)  # Ensure username is correctly used here
                )
                videos = cur.fetchall()
                for video in videos:
                    user_details['videos'].append({
                        'id': video[0],
                        'title': video[1],
                        'size': video[2],
                        'upload_time': video[3].isoformat()
                    })

                user_details_list.append(user_details)
    return user_details_list

@app.route('/search_users', methods=['GET'])
def search_users():
    username_keyword = request.args.get('username_keyword')
    if not username_keyword:
        return jsonify({'error': 'Username keyword is required'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_user_details_by_keyword, username_keyword)
        user_details_list = future.result()

    if not user_details_list:
        return jsonify({'error': 'No users found'}), 404
    return jsonify(user_details_list)





# ------------------------------------------------VIDEO--------------------------------------------------------------------





# Upload a video
def insert_video_db(title, username, video_file_path, video_size, duration_seconds, upload_time):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO videos (title, author, video_path, bytes, duration_seconds, upload_time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;',
                (title, username, video_file_path, video_size, duration_seconds, upload_time)
            )
            video_id = cur.fetchone()[0]
            conn.commit()
    return video_id

@app.route('/upload_video', methods=['POST'])
def upload_video():
    title = request.form.get('title')
    username = request.form.get('username')
    duration_seconds = request.form.get('duration')
    video_file = request.files.get('video')

    if not title or not username or not duration_seconds:
        return jsonify({'error': 'Title, username, and duration are required and cannot be empty'}), 400

    try:
        duration_seconds = int(duration_seconds)
    except ValueError:
        return jsonify({'error': 'Duration must be an integer'}), 400

    try:
        if video_file:
            filename = secure_filename(video_file.filename)
            video_file_path = os.path.join('videos', filename)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            video_file.save(temp_file.name)
            temp_file.close()

            video_size = os.path.getsize(temp_file.name)
            upload_time = datetime.utcnow()

            # 上传文件到OSS
            with open(temp_file.name, 'rb') as file_data:
                bucket.put_object(video_file_path, file_data)
            os.unlink(temp_file.name)  # 删除临时文件

            # 在另一个线程中处理数据库操作
            thread = Thread(target=insert_video_db, args=(title, username, video_file_path, video_size, duration_seconds, upload_time))
            thread.start()
            thread.join()

            return jsonify({'message': 'Video uploaded successfully'}), 202
        else:
            return jsonify({'error': 'No video file provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download_video', methods=['GET'])
def download_video():
    video_id = request.args.get('id')

    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT video_path FROM videos WHERE id = %s;', (video_id,))
            result = cur.fetchone()

            if result:
                video_path = result[0]
                video_url = bucket.sign_url('GET', video_path, 60)  # URL expires in 60 seconds
                return jsonify({'url': video_url})
            else:
                return jsonify({'error': 'Video not found'}), 404


# List all videos
def fetch_all_videos_data():
    all_videos_data = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, author, video_path, bytes, duration_seconds, upload_time FROM videos;')
            all_videos = cur.fetchall()
            for video in all_videos:
                all_videos_data.append({
                    'id': video[0],
                    'title': video[1],
                    'author': video[2],
                    'video_path': video[3],
                    'bytes': video[4],
                    'duration_seconds': video[5],
                    'upload_time': video[6].isoformat() if video[6] else None  # Handling potential NULL values
                })
    return all_videos_data

@app.route('/list_all_videos', methods=['GET'])
def list_all_videos():
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_all_videos_data)
        videos_data = future.result()
    return jsonify(videos_data)


# Search a video by ID
def fetch_video_details(video_id):
    video_details = {}
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Fetch video details
            cur.execute('SELECT v.id, v.title, u.username, v.duration_seconds, v.bytes, v.upload_time '
                        'FROM videos v JOIN users u ON v.author = u.username '
                        'WHERE v.id = %s;', (video_id,))
            video = cur.fetchone()
            if video:
                video_details = {
                    'id': video[0],
                    'title': video[1],
                    'author': video[2],
                    'duration_seconds': video[3],
                    'size': video[4],
                    'upload_time': video[5].isoformat() if video[5] else None,
                    'comments': []
                }
                # Fetch comments for the video
                cur.execute('SELECT c.id, c.user_id, c.comment_text, c.created_at, u.username '
                            'FROM comments c JOIN users u ON c.user_id = u.id '
                            'WHERE c.video_id = %s;', (video_id,))
                comments = cur.fetchall()
                for comment in comments:
                    video_details['comments'].append({
                        'id': comment[0],
                        'user_id': comment[1],
                        'username': comment[4],  # Get the username from the JOIN
                        'text': comment[2],
                        'created_at': comment[3].isoformat() if comment[3] else None
                    })
            else:
                video_details['error'] = 'Video not found'
    return video_details

@app.route('/video_details', methods=['GET'])
def video_details():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    try:
        video_id = int(video_id)
    except ValueError:
        return jsonify({'error': 'Invalid video ID format. Video ID must be an integer.'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_video_details, video_id)
        details = future.result()

    if 'error' in details:
        return jsonify({'error': details['error']}), 404
    else:
        return jsonify(details)


# Update video information
def update_video_title(video_id, new_title):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE videos SET title = %s WHERE id = %s;',
                (new_title, video_id)
            )
            updated_rows = cur.rowcount
            conn.commit()
            return updated_rows

@app.route('/update_video_title', methods=['POST'])
def update_video_title_endpoint():
    data = request.get_json()
    video_id = data.get('video_id')
    new_title = data.get('new_title')

    if not video_id or not new_title:
        return jsonify({'error': 'Video ID and new title are required'}), 400

    # Check if video_id is an integer
    try:
        video_id = int(video_id)
    except ValueError:
        return jsonify({'error': 'Video ID must be an integer'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(update_video_title, video_id, new_title)
        updated_rows = future.result()

    if updated_rows == 0:
        return jsonify({'error': 'Video not found or no update needed'}), 404
    else:
        return jsonify({'message': 'Video title updated successfully'}), 200


# Search videos by a key word
def search_videos_by_keyword(keyword):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, title, author FROM videos WHERE title LIKE %s;',
                ('%' + keyword + '%',)
            )
            videos = cur.fetchall()
            if videos:
                return [{
                    'id': video[0],
                    'title': video[1],
                    'author': video[2]
                } for video in videos]
            else:
                return {'error': 'No videos found'}

@app.route('/search_videos', methods=['GET'])
def search_videos():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(search_videos_by_keyword, keyword)
        videos_info = future.result()

    if 'error' in videos_info:
        return jsonify({'error': videos_info['error']}), 404
    else:
        return jsonify(videos_info)

access_key_id = 'LTAI5t7bnDvfxGCirU9pT1k3'
access_key_secret = 'aB5jwBhQopvWYqzyBM6kq60deT1ApH'
bucket_name = 'lutproject'
endpoint = 'oss-cn-beijing.aliyuncs.com'


# Delete a video by ID
def delete_video_from_oss(video_path):
    # OSS配置
    auth = oss2.Auth('LTAI5t7bnDvfxGCirU9pT1k3', 'aB5jwBhQopvWYqzyBM6kq60deT1ApH')
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'lutproject')

    try:
        bucket.delete_object(video_path)
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error deleting object from OSS: {str(e)}")


@app.route('/delete_video', methods=['POST'])
def delete_video():
    data = request.json
    video_id = data.get('video_id')

    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    try:
        video_id = int(video_id)  # 验证输入的video_id是否为整数
    except ValueError:
        return jsonify({'error': 'Video ID must be an integer'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # 查找视频路径
            cur.execute('SELECT video_path FROM videos WHERE id = %s;', (video_id,))
            video = cur.fetchone()
            if not video:
                return jsonify({'error': 'Video not found'}), 404

            video_path = video[0]

            # 删除数据库中的视频记录
            try:
                cur.execute('DELETE FROM videos WHERE id = %s;', (video_id,))
                conn.commit()
            except psycopg2.errors.ForeignKeyViolation:
                conn.rollback()
                return jsonify({'error': 'Video cannot be deleted, it is referenced by other items'}), 400

            try:
                delete_video_from_oss(video_path)
            except RuntimeError as e:
                conn.rollback()
                return jsonify({'error': f'Failed to delete video from storage: {str(e)}'}), 500

    return jsonify({'message': 'Video deleted successfully'}), 200

# ------------------------------------------------COMMENT--------------------------------------------------------------------

# Post comments
@app.route('/post_comment', methods=['POST'])
def post_comment():
    data = request.json
    video_id = data.get('video_id')
    user_id = data.get('user_id')
    comment_text = data.get('comment_text')

    # Validate input types for video_id and user_id
    try:
        video_id = int(video_id)  # Ensure the video_id is an integer
        user_id = int(user_id)    # Ensure the user_id is an integer
    except (TypeError, ValueError):
        return jsonify({'error': 'Video ID and User ID must be integers'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the video exists
    cur.execute('SELECT id FROM videos WHERE id = %s;', (video_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'Video not found'}), 404

    # Check if the user exists
    cur.execute('SELECT id FROM users WHERE id = %s;', (user_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    # Insert the comment
    created_at = datetime.utcnow()
    cur.execute('INSERT INTO comments (video_id, user_id, comment_text, created_at) VALUES (%s, %s, %s, %s) RETURNING id;',
                (video_id, user_id, comment_text, created_at))
    comment_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({'message': 'Comment posted successfully', 'comment_id': comment_id}), 201


# Delete a comment by ID
def delete_comment_db(comment_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM comments WHERE id = %s;', (comment_id,))
            conn.commit()
            return cur.rowcount  # Return the number of rows affected

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    data = request.json
    comment_id = data.get('comment_id')

    if not comment_id:
        return jsonify({'error': 'Comment ID is required'}), 400

    try:
        comment_id = int(comment_id)  # Ensure the ID is an integer
    except ValueError:
        return jsonify({'error': 'Comment ID must be an integer'}), 400

    # Use ThreadPoolExecutor to handle the database operation
    with ThreadPoolExecutor() as executor:
        future = executor.submit(delete_comment_db, comment_id)
        result = future.result()  # This blocks until the result is available

    if result == 0:
        return jsonify({'error': 'No comment found with the provided ID'}), 404
    else:
        return jsonify({'message': 'Comment deleted'}), 200


# List all comments
def fetch_all_comments_data():
    all_comments_data = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, video_id, user_id, comment_text, created_at FROM comments;')
            all_comments = cur.fetchall()
            for comment in all_comments:
                all_comments_data.append({
                    'id': comment[0],
                    'video_id': comment[1],
                    'user_id': comment[2],
                    'comment_text': comment[3],
                    'created_at': comment[4].isoformat() if comment[4] else None  # Handling potential NULL values
                })
    return all_comments_data

@app.route('/list_all_comments', methods=['GET'])
def list_all_comments():
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_all_comments_data)
        comments_data = future.result()
    return jsonify(comments_data)


# Search a comment by ID
def fetch_comment_details(comment_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT c.id, c.video_id, c.user_id, c.comment_text, c.created_at, u.username '
                'FROM comments c '
                'JOIN users u ON c.user_id = u.id '
                'WHERE c.id = %s;', (comment_id,))
            comment = cur.fetchone()
            if comment:
                return {
                    'id': comment[0],
                    'video_id': comment[1],
                    'user_id': comment[2],
                    'username': comment[5],
                    'comment_text': comment[3],
                    'created_at': comment[4].isoformat() if comment[4] else None
                }
            else:
                return {'error': 'Comment not found'}

@app.route('/comment_details', methods=['GET'])
def comment_details():
    comment_id = request.args.get('comment_id')
    if not comment_id:
        return jsonify({'error': 'Comment ID is required'}), 400

    # Check if the comment_id is a valid integer
    try:
        comment_id = int(comment_id)  # This will fail if comment_id is not a valid integer
    except ValueError:
        return jsonify({'error': 'Invalid comment ID. Comment ID must be an integer.'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_comment_details, comment_id)
        details = future.result()

    if 'error' in details:
        return jsonify({'error': details['error']}), 404
    else:
        return jsonify(details)


# Update a comment by ID
def update_comment_content(comment_id, new_content):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE comments SET comment_text = %s WHERE id = %s;',
                (new_content, comment_id)
            )
            updated_rows = cur.rowcount
            conn.commit()
            return updated_rows

@app.route('/update_comment', methods=['POST'])
def update_comment():
    data = request.get_json()
    comment_id = data.get('comment_id')
    new_content = data.get('new_content')

    if not comment_id or not new_content:
        return jsonify({'error': 'Comment ID and new content are required'}), 400

    # Check if comment_id is an integer
    try:
        comment_id = int(comment_id)
    except ValueError:
        return jsonify({'error': 'Comment ID must be an integer'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(update_comment_content, comment_id, new_content)
        updated_rows = future.result()

    if updated_rows == 0:
        return jsonify({'error': 'Comment not found or no update needed'}), 404
    else:
        return jsonify({'message': 'Comment updated successfully'}), 200


# Search a comment by a key word
def search_comments_by_keyword(keyword):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # This SQL joins comments with videos and users to fetch all necessary details
            cur.execute(
                """
                SELECT c.id, c.comment_text, c.created_at, v.title, u.id as user_id, u.username 
                FROM comments c
                JOIN videos v ON c.video_id = v.id
                JOIN users u ON c.user_id = u.id
                WHERE c.comment_text LIKE %s;
                """,
                ('%' + keyword + '%',)
            )
            results = cur.fetchall()
            comments = [{
                'comment_id': row[0],
                'text': row[1],
                'created_at': row[2].isoformat(),
                'video_title': row[3],
                'commenter_id': row[4],
                'commenter_username': row[5]
            } for row in results]
            return comments

@app.route('/search_comments', methods=['GET'])
def search_comments():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    with ThreadPoolExecutor() as executor:
        future = executor.submit(search_comments_by_keyword, keyword)
        comments = future.result()

    if not comments:
        return jsonify({'error': 'No comments found'}), 404
    return jsonify(comments)



if __name__ == '__main__':
    app.run(debug=True)
