import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))  # подключение к базе

conn.autocommit = True  # не требует каждый раз вызывать метод записи данных


class User:  # методы работы с таблицей users
    @staticmethod
    def create_user(login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (login, password, firstName, middleName, surName, privileged, email, phoneNumber, persPhotoData)
            VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s, %s)
        """, (login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data))

    @staticmethod
    def find_by_login(login):
        cur = conn.cursor()
        cur.execute("SELECT login, password FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()
        if user:
            return {
                'login': user[0],
                'password': user[1]
            }
        return None


class Post:  # методы работы с таблицей posts
    @staticmethod
    def create_post(user_login, title, content, tags, image_data):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO posts (user_login, title, content, tags, createdAt, imageData, viewCount, likesCount, dislikesCount)
            VALUES (%s, %s, %s, %s, NOW(), %s, 0, 0, 0)
            RETURNING id;
        """, (user_login, title, content, tags, image_data))
        post_id = cur.fetchone()[0]

        return post_id

    @staticmethod
    def get_all_posts(order='desc', page=1, limit=0, search=''):
        offset = (page - 1) * limit  # смещение пагинации

        query = f'SELECT * FROM posts '

        if search != '':
            query += f"WHERE content LIKE '%{search}%' or title LIKE '%{search}%' or tags LIKE '%{search}%' "
        
        query += f'ORDER BY createdAt {order} '
        
        if limit != 0:
            query += f'LIMIT {limit} OFFSET {offset};'

        cur = conn.cursor()
        cur.execute(query)
        posts = cur.fetchall()
        return posts

    @staticmethod
    def get_post_by_id(post_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
        post = cur.fetchone()
        if post:
            return {
                'id': post[0],
                'user_login': post[1],
                'title': post[2],
                'content': post[3],
                'tags': post[4],
                'createdAt': post[5],
                'imageData': post[6],
                'viewCount': post[7],
                'likesCount': post[8],
                'dislikesCount': post[9]
            }
        return None

    @staticmethod
    def update_post(post_id, title, content, tags, image_data):
        cur = conn.cursor()
        cur.execute("""
            UPDATE posts
            SET title = %s, content = %s, tags = %s, imageData = %s
            WHERE id = %s;
        """, (title, content, tags, image_data, post_id))

    @staticmethod
    def delete_post(post_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE id = %s;", (post_id,))

    @staticmethod
    def increment_view(post_id):
        cur = conn.cursor()
        cur.execute("UPDATE posts SET view_count = view_count + 1 WHERE id = %s", (post_id,))

    @staticmethod
    def like_post(post_id):
        cur = conn.cursor()
        cur.execute("UPDATE posts SET likes_count = likes_count + 1 WHERE id = %s", (post_id,))

    @staticmethod
    def dislike_post(post_id):
        cur = conn.cursor()
        cur.execute("UPDATE posts SET dislikes_count = dislikes_count + 1 WHERE id = %s", (post_id,))


class Comment:  # методы работы с таблицей comments
    @staticmethod
    def create_comment(user_login, post_id, content, image_data, tags):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comments (user_login, post_id, content, imageData, tags, createdAt)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id;
        """, (user_login, post_id, content, image_data, tags))
        comment_id = cur.fetchone()[0]

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

        cur = conn.cursor()
        cur.execute(query, (post_id, limit, offset))
        comments = cur.fetchall()
        return comments

    @staticmethod
    def get_comment_by_id(comment_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM comments WHERE id = %s;", (comment_id,))
        comment = cur.fetchone()
        if comment:
            return {
                'id': comment[0],
                'user_login': comment[1],
                'post_id': comment[2],
                'content': comment[3],
                'imageData': comment[4],
                'tags': comment[5],
                'createdAt': comment[6]
            }
        return None

    @staticmethod
    def update_comment(comment_id, content, image_data, tags):
        cur = conn.cursor()
        cur.execute("""
            UPDATE comments
            SET content = %s, imageData = %s, tags = %s
            WHERE id = %s;
        """, (content, image_data, tags, comment_id))

    @staticmethod
    def delete_comment(comment_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM comments WHERE id = %s;", (comment_id,))

