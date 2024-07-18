from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
import uuid  # библиотека генерации уникальных идентификаторов (UUID)
import time
import os

load_dotenv()

AUTHORIZATION_LIMIT = os.getenv("AUTHORIZATION_LIMIT")


def generate_uuid():  # метод генерация уникального идентификатора
    return str(uuid.uuid4())


def create_user_jwt_token(login: str, password: str) -> str:  # мой метод создания токена авторизации
    authorization_limit = int(time.time())
    token = create_access_token(identity={"created_time": authorization_limit, "login": login, "password": password})
    return token


def encrypt_decrypt(text: str, key: str) -> str:  # шифрование и дешифрование текста капчи

    # Преобразуем строку в байтовый массив, чтобы работать с кодами символов (ASCII)
    text_bytes = bytearray(text, 'utf-8')
    key_bytes = bytearray(key, 'utf-8')

    encrypted_bytes = bytearray()  # Создаем пустой байтовый массив для хранения зашифрованного текста

    # Циклически применяем XOR к каждому байту текста с соответствующим байтом ключа
    for i in range(len(text_bytes)):
        encrypted_byte = text_bytes[i] ^ key_bytes[i % len(key_bytes)]
        encrypted_bytes.append(encrypted_byte)

    # Преобразуем зашифрованный байтовый массив обратно в строку и возвращаем результат
    encrypted_text = encrypted_bytes.decode('utf-8')
    return encrypted_text

