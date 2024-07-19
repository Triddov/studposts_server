from flask import Flask
from .config import config
from .extensions import jwt, redis_store
from .database import init_db
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окружения из .env файла


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    # Настройки приложения
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # Замените на ваш секретный ключ
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    # Инициализация расширений
    jwt.init_app(app)

    # Инициализация базы данных
    with app.app_context():
        init_db()

    # Регистрация блюпринтов
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
