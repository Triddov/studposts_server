from flask import Flask
from flask_jwt_extended import JWTManager  # Либа для управления JWT-токенами (для аутентификации и авторизации)
from .database import init_db
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окружения из .env файла

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    # Инициализация расширений
    jwt.init_app(app)

    # Инициализация базы данных
    with app.app_context():
        init_db()

    # Регистрация блюпринтов (в раутах будет префикс api)
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
