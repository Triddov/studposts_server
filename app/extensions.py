from flask_jwt_extended import JWTManager
import redis

jwt = JWTManager()
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
