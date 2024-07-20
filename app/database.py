import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))  # подключение к базе

conn.autocommit = True  # не требует каждый раз вызывать метод записи данных


class User:  # методы работы с таблицей users
    @staticmethod
    def create_user(login, password, first_name, sur_name, middle_name=None, email=None, phone_number=None,
                    pers_photo_data=None):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (login, password, firstName, middleName, surName, privileged, email, phoneNumber, persphotodata)
            VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s, %s)
            RETURNING login, firstName, middleName, surName, privileged, email, phoneNumber, persphotodata
        """, (login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data))

        user_data = cur.fetchone()

        response = {}

        # Extracting each field and adding to the response dictionary only if it's not None
        fields = ['login', 'firstName', 'middleName', 'surName', 'privileged', 'email', 'phoneNumber', 'persPhotodata']
        for i, field in enumerate(fields):
            if user_data[i] is not None:
                response[field] = user_data[i]

        return response

    @staticmethod
    def get_user(login):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user_data = cur.fetchone()
        response = {
            'login': user_data[0],
            'firstName': user_data[2],
            'surName': user_data[3],
            'middleName': user_data[4],
            'privileged': user_data[5],
            'email': user_data[6],
            'phoneNumber': user_data[7],
            'persPhotodata': user_data[8]
        }
        return response

    @staticmethod
    def is_moderator(login):
        cur = conn.cursor()
        cur.execute("SELECT privileged FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()
        return user[0]

    @staticmethod
    def find_by_login(login):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user_data = cur.fetchone()
        if user_data:
            response = {
                'login': user_data[0],
                'password': user_data[1],
                'firstName': user_data[2],
                'surName': user_data[3],
                'middleName': user_data[4],
                'privileged': user_data[5],
                'email': user_data[6],
                'phoneNumber': user_data[7],
                'persPhotodata': user_data[8]
            }
            return response
        else:
            return False

    @staticmethod
    def update_user(original_login, login=None, password=None, first_name=None, middle_name=None, sur_name=None,
                    email=None, phone_number=None, pers_photo_data=None):
        cur = conn.cursor()
        fields = []

        update_fields = {
            "login": login,
            "password": password,
            "firstName": first_name,
            "middleName": middle_name,
            "surName": sur_name,
            "email": email,
            "phoneNumber": phone_number,
            "persPhotoData": pers_photo_data
        }

        for field, value in update_fields.items():
            if value:
                fields.append(f"{field} = '{value}'")

        if fields:

            query = f"UPDATE users SET {', '.join(fields)} WHERE login = '{original_login}';"
            cur.execute(query)

        else:
            raise Exception  # данных не поступило


class Post:  # методы работы с таблицей posts
    @staticmethod
    def create_post(unique_id, owner_login, title, content, tags, image_data):
        cur = conn.cursor()
        cur.execute("""INSERT INTO posts (unique_id, owner_login, title, content, tags, createdAt, imageData, viewCount, likesCount, dislikesCount)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s, 0, 0, 0)""", (unique_id, owner_login, title, content, tags, image_data))

    @staticmethod
    def get_all_posts(order='desc', page=1, limit=0, search=None):
        offset = (page - 1) * limit  # смещение пагинации

        query = f"SELECT * FROM posts "

        if search:
            query += f"WHERE content LIKE '%{search}%' or title LIKE '%{search}%' or tags LIKE '%{search}%' "

        query += f"ORDER BY createdAt {order} "

        if limit != 0:
            query += f"LIMIT {limit} OFFSET {offset};"

        cur = conn.cursor()
        cur.execute(query)
        posts = cur.fetchall()
        return posts

    @staticmethod
    def get_post_by_id(unique_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts WHERE unique_id = %s;", (unique_id,))
        post = cur.fetchone()
        return post

    @staticmethod
    def update_post(unique_id, owner_login, **field):
        cur = conn.cursor()

        # Сначала проверяем, что логин пользователя совпадает с логином создателя поста
        cur.execute("SELECT owner_login FROM posts WHERE unique_id = %s", (unique_id,))
        result = cur.fetchone()

        if result and result[0] == owner_login:
            # Если логины совпадают, обновляем пост
            fields = [f"{key} = %s" for key in field if field[key] is not None]
            values = [field[key] for key in field if field[key] is not None]

            if fields:
                values.append(unique_id)
                query = f"UPDATE posts SET {', '.join(fields)} WHERE unique_id = %s;"
                cur.execute(query, values)
                conn.commit()
        else:
            raise Exception

    @staticmethod
    def delete_post(unique_id, owner_login):
        cur = conn.cursor()

        # Сначала проверяем, что логин пользователя совпадает с логином создателя поста
        cur.execute("SELECT owner_login FROM posts WHERE unique_id = %s", (unique_id,))
        user = cur.fetchone()

        cur.execute("SELECT privileged FROM users WHERE login = %s", (owner_login,))
        privileged = cur.fetchone()

        if (user and user[0] == owner_login) or privileged:
            cur.execute("DELETE FROM posts WHERE unique_id = %s;", (unique_id,))
        else:
            raise Exception

    @staticmethod
    def image_already(post_id):
        cur = conn.cursor()
        cur.execute("SELECT imagedata FROM posts WHERE unique_id = %s;", (post_id,))
        already_exists = cur.fetchone()
        return True if already_exists else False

    @staticmethod
    def image_filename(post_id):
        cur = conn.cursor()
        cur.execute("SELECT imagedata FROM posts WHERE unique_id = %s;", (post_id,))
        result = cur.fetchone()

        if result:
            return os.path.basename(result[0])
        else:
            raise Exception

    @staticmethod
    def increment_view(post_id):
        cur = conn.cursor()
        cur.execute("UPDATE posts SET viewcount = viewcount + 1 WHERE unique_id = %s", (post_id,))

    @staticmethod
    def like_post(login, post_id, action):
        cur = conn.cursor()

        if action == 'like':
            cur.execute(f"SELECT * FROM likes WHERE post_id = '{post_id}' and owner_login = '{login}';")
            if cur.fetchone():
                return False, 'like has already been set'

            cur.execute(f"INSERT INTO likes (owner_login, post_id) VALUES ('{login}', '{post_id}');")

            cur.execute(f"DELETE FROM dislikes WHERE post_id = '{post_id}' and owner_login = '{login}';")

        elif action == 'unlike':
            cur.execute(f"SELECT * FROM likes WHERE post_id = '{post_id}' and owner_login = '{login}';")
            if not cur.fetchone():
                return False, "like hasn't been set"

            cur.execute(f"DELETE FROM likes WHERE post_id = '{post_id}' and owner_login = '{login}';")

        return True, None

    @staticmethod
    def dislike_post(login, post_id, action):
        cur = conn.cursor()

        if action == 'dislike':
            cur.execute(f"SELECT * FROM dislikes WHERE post_id = '{post_id}' and owner_login = '{login}';")
            if cur.fetchone():
                return False, 'dislike has already been set'

            cur.execute(f"INSERT INTO dislikes (owner_login, post_id) VALUES ('{login}', '{post_id}');")

            cur.execute(f"DELETE FROM likes WHERE post_id = '{post_id}' and owner_login = '{login}';")

        elif action == 'undislike':
            cur.execute(f"SELECT * FROM dislikes WHERE post_id = '{post_id}' and owner_login = '{login}';")
            if not cur.fetchone():
                return False, "dislike hasn't been set"

            cur.execute(f"DELETE FROM dislikes WHERE post_id = '{post_id}' and owner_login = '{login}';")

        return True, None


class Comment:  # методы работы с таблицей comments
    @staticmethod
    def create_comment(unique_id, owner_login, post_id, content):
        cur = conn.cursor()

        # Проверяем, существует ли пост с указанным post_id
        cur.execute("SELECT 1 FROM posts WHERE unique_id = %s", (post_id,))
        post_exists = cur.fetchone()

        # Создаем комментарий, если пост существует
        if post_exists:
            cur.execute("""
                INSERT INTO comments (unique_id, owner_login, post_id, content, createdAt)
                VALUES (%s, %s, %s, %s, NOW())
            """, (unique_id, owner_login, post_id, content))
            conn.commit()
        else:
            raise Exception

    @staticmethod
    def get_comments_by_post(post_id, order='desc', page=1, limit=0):
        offset = (page - 1) * limit  # смещение пагинации

        # Используйте параметризованный запрос для безопасности и правильной обработки типов данных
        query = """
            SELECT * FROM comments
            WHERE post_id = %s
            ORDER BY createdAt """ + order

        if limit != 0:
            query += f' LIMIT {limit} OFFSET {offset};'

        cur = conn.cursor()
        cur.execute(query, (post_id,))
        comments = cur.fetchall()
        print(comments)
        return comments

    @staticmethod
    def get_comment_by_id(comment_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM comments WHERE unique_id = %s;", (comment_id,))
        comment = cur.fetchone()
        return comment

    @staticmethod
    def update_comment(comment_id, owner_login, content):
        cur = conn.cursor()

        cur.execute("SELECT owner_login FROM comments WHERE unique_id = %s", (comment_id,))
        result = cur.fetchone()

        if result and result[0] == owner_login:
            cur.execute("""
                UPDATE comments
                SET content = %s
                WHERE unique_id = %s;
            """, (content, comment_id))
        else:
            raise Exception

    @staticmethod
    def delete_comment(comment_id, owner_login):

        cur = conn.cursor()
        cur.execute("SELECT owner_login FROM comments WHERE unique_id = %s", (comment_id,))
        user = cur.fetchone()

        cur.execute("SELECT privileged FROM users WHERE login = %s", (owner_login,))
        privileged = cur.fetchone()

        if (user and user[0] == owner_login) or privileged:
            cur.execute("DELETE FROM comments WHERE unique_id = %s;", (comment_id,))
        else:
            raise Exception

