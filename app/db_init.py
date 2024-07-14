from database import get_db_connection


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        login VARCHAR(255) PRIMARY KEY,
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
        user_login VARCHAR(255) NOT NULL,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        imageData VARCHAR(255),
        viewCount INTEGER DEFAULT 0,
        likesCount INTEGER DEFAULT 0,
        dislikesCount INTEGER DEFAULT 0,
        FOREIGN KEY (user_login) REFERENCES users (login)
    );
    
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        user_login VARCHAR(255) NOT NULL,
        post_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_login) REFERENCES users (login),
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );""")
    conn.commit()  # сохранение изменений в базу
    cur.close()
    conn.close()
