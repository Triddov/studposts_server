from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required, decode_token
from functools import wraps
from .database import User, Post, Comment
from .generate_captcha import generate_captcha, generate_captcha_image
from .generate_token import encrypt_decrypt, generate_unique_token
from .check_data import check_user_data, check_post_data, check_comment_data, is_image_square
from .server_exception import Response
from dotenv import load_dotenv
import time
import os

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
TIME_CAPTCHA_LIMIT = int(os.getenv('JWT_EXPIRATION_MINUTES'))

api = Blueprint('api', __name__)
jwt = JWTManager()  # объект генерации токенов


# Первоочередное:

# проверять данные юзера, постов, комментов и (главное блять) фоток (это фото, размер, квадратное)
# генерировать названия постов, картинок и ключей
# процедура проверки названий иконок

# Потом:

# волюм для sourses


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        response = Response()

        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            response.status(405)
            return response.send()

        try:
            get_jwt_identity()  # будет ошибка, если токен недействителен
        except:
            response.set_status(406)
            return response.send()
        return f(*args, **kwargs)
    return decorator


@api.route('/captcha', methods=['GET'])
def get_captcha():
    response = Response()

    captcha_text = generate_captcha()
    encoded_captcha_solution = encrypt_decrypt(captcha_text, SECRET_KEY)
    base64_image = generate_captcha_image(captcha_text)
    print("Текст капчи: " + captcha_text)
    token = create_access_token(identity={'captcha_solution': encoded_captcha_solution})
    time_generate_captcha = int(time.time()*1000)  # в миллисекундах

    response.set_header("Time-Generate-Captcha", time_generate_captcha)
    response.set_data({
        'captcha_image': base64_image,  # изображение капчи, закодированное в base64
        'captcha_solution_token': token  # закодированное решение капчи в виде jwt-токен
    })

    return response.send()


@api.route('/auth', methods=['POST'])
def auth():
    response = Response()
    try:
        action = request.headers.get('Target-Action')
        captcha_time = int(request.headers.get('Time-Generate-Captcha'))
        data = request.get_json()

        captcha_token = data.get("captcha_token")
        input_captcha = data.get("input_captcha")

        if not captcha_token or not input_captcha:
            response.set_data({"msg": "Captcha required"})
            response.set_status(411)
            return response.send()

        current_time = int(time.time()*1000)  # в миллисекундах

        if (current_time-captcha_time) > TIME_CAPTCHA_LIMIT:
            response.set_data({"msg": "Exceeded time captcha limit"})
            response.set_status(416)
            return response.send()

        try:
            decoded_token = decode_token(captcha_token)
            captcha_solution = encrypt_decrypt(decoded_token['sub']['captcha_solution'], SECRET_KEY)

        except:
            response.set_status(413)
            response.set_data({"msg": "Invalid captcha token"})
            return response.send()

        if input_captcha != captcha_solution:  # проверка решения капчи
            response.set_data({"msg": "Invalid captcha solution"})
            response.set_status(414)
            return response.send()

        if action == 'REGISTER':
            login = data.get('login')
            password = data.get('password')
            first_name = data.get('first_name')
            middle_name = data.get('middle_name')
            sur_name = data.get('sur_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            pers_photo_data = data.get('pers_photo_data')

            if User.find_by_login(login):
                response.set_data({"msg": "Already exist"})
                response.set_status(409)
                return response.send()

            user_login = User.create_user(login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data)
            unique_token = generate_unique_token()
            access_token = create_access_token(identity=unique_token)

            response.set_data({
                "msg": "User registered successfully",
                "user_login": user_login,
                "session_key": access_token
            })

            return response.send()

        elif action == 'LOGIN':
            login = data.get('login')
            password = data.get('password')
            user = User.find_by_login(login)

            if user and user['password'] == password:
                unique_token = generate_unique_token()
                access_token = create_access_token(identity=unique_token)

                response.set_data({
                    "msg": "User registered successfully",
                    "session_key": access_token
                })
                return response.send()

        else:
            response.set_status(415)
            response.set_data({"msg": "Incorrect action"})
            return response.send()

    except Exception as err:
        response.set_message(err)
        response.set_status(400)
        return response.send()

    @api.route('/posts/', methods=['GET'])
    def handle_posts():
        pass

    @api.route('/post/create/', methods=['POST'])
    @jwt_required()
    def new_post():
        pass

    @api.route('/post/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    def handle_post(id):
        pass

    @api.route('/post/<int:post_id>/comments/', methods=['GET'])
    def handle_comments(post_id):
        pass

    @api.route('/post/<int:post_id>/comment/create/', methods=['POST'])
    @jwt_required()
    def new_comment():
        pass

    @api.route('/post/<int:post_id>/comment/<int:id>/', methods=['PUT', 'DELETE'])
    @jwt_required()
    def handle_comment(id):
        pass

    @api.route('/posts/<int:post_id>/view', methods=['PUT'])
    def update_view_count(post_id):
        pass

    @api.route('/posts/<int:post_id>/like', methods=['PUT'])
    def update_likes_count(post_id):
        pass

    @api.route('/posts/<int:post_id>/dislike', methods=['PUT'])
    def update_dislikes_count(post_id):
        pass

