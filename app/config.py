import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env файла


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
