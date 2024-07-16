from flask import Flask
from flask_jwt_extended import JWTManager  # библиотека для управления JWT-токенами (для аутентификации и авторизации)
from .badwords_checker import BannedWordsChecker
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()  # Загрузка переменных окружения из .env файла

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Инициализация расширений
    jwt.init_app(app)

    # Инициализация плохих слов
    BannedWordsChecker.load_banned_words()

    # Регистрация блюпринтов (в раутах будет префикс api)
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
