from flask import Flask
from flask_jwt_extended import JWTManager  # Либа для управления JWT-токенами (для аутентификации и авторизации)
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()  # Загрузка переменных окружения из .env файла

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=int(os.getenv('JWT_EXPIRATION_MINUTES', default=5)))

    # Инициализация расширений
    jwt.init_app(app)

    # Регистрация блюпринтов (в раутах будет префикс api)
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
