-- Database: STUDPOSTS

    CREATE TABLE IF NOT EXISTS users (
        login VARCHAR(255) PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        firstName VARCHAR(50) NOT NULL,
        surName VARCHAR(50) NOT NULL,
        middleName VARCHAR(50),
        privileged BOOLEAN DEFAULT FALSE,
        email VARCHAR(36),
        phoneNumber VARCHAR(20),
        persPhotoData VARCHAR(255) DEFAULT 'sources/userProfileIcons/default_user_icon.png' NOT NULL
    );

    CREATE TABLE IF NOT EXISTS posts (
        unique_id VARCHAR(50) PRIMARY KEY,
        owner_login VARCHAR(255) NOT NULL,
        title VARCHAR(200) NOT NULL,
        content VARCHAR(5000) NOT NULL,
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        imageData VARCHAR(255),
        viewCount INTEGER DEFAULT 0,
        likesCount INTEGER DEFAULT 0,
        dislikesCount INTEGER DEFAULT 0,
        FOREIGN KEY (owner_login) REFERENCES users (login)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS comments (
        unique_id VARCHAR(50) PRIMARY KEY,
        owner_login VARCHAR(255) NOT NULL,
        post_id VARCHAR(50) NOT NULL,
        content VARCHAR(5000) NOT NULL,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_login) REFERENCES users (login)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts (unique_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS likes (
        owner_login VARCHAR(255) NOT NULL,
        post_id VARCHAR(50) NOT NULL,
        FOREIGN KEY (owner_login) REFERENCES users (login)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts (unique_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS dislikes (
        owner_login VARCHAR(255) NOT NULL,
        post_id VARCHAR(50) NOT NULL,
        FOREIGN KEY (owner_login) REFERENCES users (login)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts (unique_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );

    CREATE OR REPLACE FUNCTION changeLikesCount()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                UPDATE posts
                SET likesCount = (SELECT COUNT(*) FROM likes WHERE post_id = OLD.post_id)
                WHERE unique_id = OLD.post_id;
                
                DELETE FROM dislikes WHERE post_id = OLD.post_id and owner_login = OLD.owner_login;
                
                
            ELSIF (TG_OP = 'INSERT') THEN
                UPDATE posts
                SET likesCount = (SELECT COUNT(*) FROM likes WHERE post_id = NEW.post_id)
                WHERE unique_id = NEW.post_id; 
                
                DELETE FROM dislikes WHERE post_id = NEW.post_id and owner_login = NEW.owner_login;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER tgrChangeLikesCount
        AFTER DELETE OR INSERT ON likes
        FOR EACH ROW
        EXECUTE FUNCTION changeLikesCount();
    
    CREATE OR REPLACE FUNCTION changeDislikesCount()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                UPDATE posts
                SET dislikesCount = (SELECT COUNT(*) FROM dislikes WHERE post_id = OLD.post_id)
                WHERE unique_id = OLD.post_id;
            ELSIF (TG_OP = 'INSERT') THEN
                UPDATE posts
                SET dislikesCount = (SELECT COUNT(*) FROM dislikes WHERE post_id = NEW.post_id)
                WHERE unique_id = NEW.post_id; 
                
                DELETE FROM likes WHERE post_id = NEW.post_id and owner_login = NEW.owner_login;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER tgrChangeDislikesCount
        AFTER DELETE OR INSERT ON dislikes
        FOR EACH ROW
        EXECUTE FUNCTION changeDislikesCount();


INSERT INTO users (login, password, firstName, middleName, surName, privileged, persphotodata)
VALUES ('dima', 'qwerty12345', 'Дмитрий', 'Иванович', 'Путин', TRUE, 'sources/userProfileIcons/dima-image.png');

INSERT INTO users (login, password, firstName, middleName, surName, privileged, email, phoneNumber, persphotodata)
VALUES ('step', 'qwerty09876', 'Степан', 'Иванович', 'Путин', TRUE, 'akinin.stepan7@gmail.com', '+71987464539', 'sources/userProfileIcons/stepa-image.png');

INSERT INTO users (login, password, firstName, middleName, surName, privileged, email, persphotodata)
VALUES ('ye', 'ye123456', 'Канье', 'Иванович', 'Уэст', TRUE, 'ye@gmail.com', 'sources/userProfileIcons/ye-image.png');