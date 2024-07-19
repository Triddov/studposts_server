import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app


def get_db_connection():
    conn = psycopg2.connect(current_app.config['DATABASE_URL'], cursor_factory=RealDictCursor)
    return conn


class User:
    @staticmethod
    def create_user(username, password, first_name, last_name, session_key, email, phone_number, pers_photo_data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password, firstName, lastName, sessionKey, privileged, email, phoneNumber, persPhotoData)
            VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s, %s)
            RETURNING id;
        """, (username, password, first_name, last_name, session_key, email, phone_number, pers_photo_data))
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return user_id

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user


class Post:
    @staticmethod
    def create_post(user_id, title, content, tags, image_data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO posts (user_id, title, content, tags, createdAt, imageData, viewCount, likesCount, dislikesCount)
            VALUES (%s, %s, %s, %s, NOW(), %s, 0, 0, 0)
            RETURNING id;
        """, (user_id, title, content, tags, image_data))
        post_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return post_id

    @staticmethod
    def get_all_posts():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts;")
        posts = cur.fetchall()
        cur.close()
        conn.close()
        return posts

    @staticmethod
    def get_post_by_id(post_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
        post = cur.fetchone()
        cur.close()
        conn.close()
        return post

    @staticmethod
    def update_post(post_id, title, content, tags, image_data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE posts
            SET title = %s, content = %s, tags = %s, imageData = %s
            WHERE id = %s;
        """, (title, content, tags, image_data, post_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_post(post_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE id = %s;", (post_id,))
        conn.commit()
        cur.close()
        conn.close()


class Comment:
    @staticmethod
    def create_comment(user_id, post_id, content, image_data, tags):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comments (user_id, post_id, content, imageData, tags, createdAt)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id;
        """, (user_id, post_id, content, image_data, tags))
        comment_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return comment_id

    @staticmethod
    def get_comments_by_post(post_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM comments WHERE post_id = %s;", (post_id,))
        comments = cur.fetchall()
        cur.close()
        conn.close()
        return comments

    @staticmethod
    def update_comment(comment_id, content, image_data, tags):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE comments
            SET content = %s, imageData = %s, tags = %s
            WHERE id = %s;
        """, (content, image_data, tags, comment_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_comment(comment_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM comments WHERE id = %s;", (comment_id,))
        conn.commit()
        cur.close()
        conn.close()
