import psycopg2
from psycopg2.extras import RealDictCursor  # метод возвращения запросов как dict (а не tuple)
from flask import current_app


def get_db_connection():
    conn = psycopg2.connect(current_app.config['DATABASE_URL'], cursor_factory=RealDictCursor)
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(120) NOT NULL,
        password VARCHAR(128) NOT NULL,
        firstName VARCHAR(50),
        lastName VARCHAR(50),
        privileged BOOLEAN DEFAULT FALSE,
        email VARCHAR(36) NOT NULL,
        phoneNumber VARCHAR(20),
        persPhotoData VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        imageData VARCHAR(255),
        viewCount INTEGER DEFAULT 0,
        likesCount INTEGER DEFAULT 0,
        dislikesCount INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        imageData VARCHAR(255),
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    """)
    conn.commit()  # сохранение изменений в базу
    cur.close()
    conn.close()


class User:
    @staticmethod
    def create_user(username, password, first_name, last_name, email, phone_number, pers_photo_data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password, firstName, lastName, privileged, email, phoneNumber, persPhotoData)
            VALUES (%s, %s, %s, %s, FALSE, %s, %s, %s)
            RETURNING id;
        """, (username, password, first_name, last_name, email, phone_number, pers_photo_data))
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

        return user_id

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = %s;", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'password': user[2]
            }
        return None


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
    def get_all_posts(sort='date', order='desc', page=1, limit=10):
        offset = (page - 1) * limit  # смещение пагинации

        valid_sort_fields = {'date', 'author', 'title', 'content'}
        if sort not in valid_sort_fields:
            sort = 'date'  # сортировка по умолчанию, если поле неверное

        valid_order_values = {'asc', 'desc'}
        if order not in valid_order_values:
            order = 'desc'  # сортировка по умолчанию, если поле неверное

        query = f"""
            SELECT * FROM posts
            ORDER BY {sort} {order}
            LIMIT %s OFFSET %s;
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (limit, offset))
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
    def get_comments_by_post(post_id, sort='date', order='desc', page=1, limit=10):
        offset = (page - 1) * limit  # смещение пагинации

        valid_sort_fields = {'date', 'author', 'content'}  # допустимые поля сортировки
        if sort not in valid_sort_fields:
            sort = 'date'  # сортировка по умолчанию, если поле неверное

        valid_order_values = {'asc', 'desc'}  # допустимые значения порядка сортировки
        if order not in valid_order_values:
            order = 'desc'  # сортировка по умолчанию, если поле неверное

        query = f"""
            SELECT * FROM comments
            WHERE post_id = %s
            ORDER BY {sort} {order}
            LIMIT %s OFFSET %s;
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (post_id, limit, offset))
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
