from flask_jwt_extended import JWTManager  # Либа для управления JWT-токенами (для аутентификации и авторизации)
import redis

jwt = JWTManager()
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)  # decode_responses - все ответы будут декодированы в строки
