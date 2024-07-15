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
TIME_CAPTCHA_LIMIT = int(os.getenv('JWT_EXPIRATION_MINUTES')) * 60000  # в миллисекундах

api = Blueprint('api', __name__)  # добавляет api во всех раутах
jwt = JWTManager()  # объект генерации токенов


# Задачи (не забыть блять):

# проверять данные юзера, постов, комментов и (главное блять) фоток (это фото, размер, квадратное)
# генерировать названия постов, картинок и ключей
# процедура проверки названий иконок
# волюм для sourses

def token_required(f):  # метод проверки токенов авторизации пользователя
    @wraps(f)
    def decorator(*args, **kwargs):  # декоратор для проверки токена на каждом рауте
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


@api.route('/captcha', methods=['GET'])  # метод генерации и получения капчи
def get_captcha():
    response = Response()

    # генерация капчи
    captcha_text = generate_captcha()
    encoded_captcha_solution = encrypt_decrypt(captcha_text, SECRET_KEY)
    base64_image = generate_captcha_image(captcha_text)
    print("Текст капчи: " + captcha_text)
    captcha_actual_time = int(time.time() * 1000) + TIME_CAPTCHA_LIMIT  # время, до которого капча валидна
    token = create_access_token(identity={"solution": encoded_captcha_solution, "actual_time": captcha_actual_time})

    response.set_data({
        'captcha_image': base64_image,  # изображение капчи, закодированное в base64
        'captcha_token': token  # закодированное решение капчи в виде jwt-токен
    })
    return response.send()


@api.route('/auth', methods=['POST'])  # метод авторизации/регистрации пользователя
def auth():
    response = Response()
    try:
        action = request.headers.get('Target-Action')  # значение Target-Action заголовка запроса

        data = request.get_json()
        input_captcha = data.get("input_captcha")
        captcha_solution_token = data.get("captcha_token")

        if not captcha_solution_token or not input_captcha:
            response.set_status(411)
            return response.send()

        try:
            decoded_captcha_token = decode_token(captcha_solution_token)
            captcha_solution = encrypt_decrypt(decoded_captcha_token['sub']['solution'], SECRET_KEY)
            captcha_actual_time = decoded_captcha_token['sub']['actual_time']

        except:
            response.set_status(413)
            return response.send()

        current_time = int(time.time() * 1000)  # в миллисекундах

        if captcha_actual_time < current_time:
            response.set_status(416)
            return response.send()

        if input_captcha != captcha_solution:  # проверка решения капчи
            response.set_status(414)
            return response.send()

        if action == 'REGISTER':
            try:
                login = data.get('login')
                password = data.get('password')
                first_name = data.get('first_name')
                middle_name = data.get('middle_name')
                sur_name = data.get('sur_name')
                email = data.get('email')
                phone_number = data.get('phone_number')
                pers_photo_data = data.get('pers_photo_data')

                is_valid, validation_error = check_user_data(data)

            except Exception:
                response.set_status(417)
                return response.send()

            try:
                if is_valid:
                    if User.find_by_login(login):
                        response.set_status(409)
                        return response.send()

                    user_login = User.create_user(login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data)
                    unique_token = generate_unique_token()
                    access_token = create_access_token(identity=unique_token)

                    if validation_error is not None:
                        response.set_status(417)
                        response.set_message(validation_error)
                        return response.send()

                    response.set_data({
                        "user_login": user_login,
                        "session_key": access_token
                    })

                    return response.send()

                else:
                    response.set_status(417)
                    response.set_message(validation_error)
                    return response.send()

            except Exception:
                response.set_status(504)
                return response.send()

        elif action == 'LOGIN':
            try:
                login = data.get('login')
                password = data.get('password')
            except:
                response.set_status(417)
                return response.send()

            try:
                user = User.find_by_login(login)

            except Exception:
                response.set_status(504)
                return response.send()

            if user and user['password'] == password:
                unique_token = generate_unique_token()
                access_token = create_access_token(identity=unique_token)

                response.set_data({
                    "msg": "User registered successfully",
                    "session_key": access_token
                })
                return response.send()

            else:
                response.set_status(417)
                return response.send()

        else:
            response.set_status(415)
            return response.send()

    except Exception as err:
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

