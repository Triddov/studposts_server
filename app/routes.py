from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required, decode_token
from .database import User, Post, Comment
from .generate_captcha import generate_captcha, generate_captcha_image
from .generate_token import encrypt_decrypt, generate_uuid, create_user_jwt_token
from .validation_data import *
from .server_exception import Response
from .badwords_checker import BannedWordsChecker
from dotenv import load_dotenv
from functools import wraps
import time
import os

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
TIME_CAPTCHA_LIMIT = int(os.getenv('JWT_EXPIRATION_MINUTES')) * 60000  # в миллисекундах

api = Blueprint('api', __name__)  # добавляет api во всех раутах
jwt = JWTManager()  # объект генерации токенов


# Задачи (не забыть блять):

# сделать эндпоинты для постов и комментов (ден и сергей)
# протестить методы проверки постов и комментов
# генерировать названия постов
# волюм для sourses


def token_required(f):  # метод проверки токенов авторизации
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
        # получаем значение Target-Action в заголовке запроса
        action = request.headers.get('Target-Action')

        data = request.get_json()
        input_captcha = data.get("input_captcha")
        captcha_solution_token = data.get("captcha_token")

        # проверка наличия полей решения капчи
        if not captcha_solution_token or not input_captcha:
            response.set_status(411)
            return response.send()

        # декодируем капчу и время, до которого она валидна
        try:
            decoded_captcha_token = decode_token(captcha_solution_token)
            captcha_solution = encrypt_decrypt(decoded_captcha_token['sub']['solution'], SECRET_KEY)
            captcha_actual_time = decoded_captcha_token['sub']['actual_time']

        except:
            response.set_status(413)
            return response.send()

        current_time = int(time.time() * 1000)  # в миллисекундах

        # проверка актуального времени капчи
        if captcha_actual_time < current_time:
            response.set_status(416)
            return response.send()

        # проверка пользовательского решения капчи
        if input_captcha != captcha_solution:
            response.set_status(414)
            return response.send()

        # логика регистрации
        if action == 'REGISTER':
            try:
                # публичные поля (требуют проверки на badwords)
                first_name = data.get('first_name')
                middle_name = data.get('middle_name')
                sur_name = data.get('sur_name')

                # непубличные поля (не требуют проверки на badwords)
                login = data.get('login')
                password = data.get('password')
                email = data.get('email')
                phone_number = data.get('phone_number')
                pers_photo_data = data.get('pers_photo_data')
                header, pers_photo_data = pers_photo_data.split(",", 1)

                # валидация все полей
                is_valid, validation_error = check_user_data(data)
                if not is_valid:
                    response.set_status(417)
                    response.set_message(validation_error)
                    return response.send()

                # проверка на плохие слова
                first_name = BannedWordsChecker.bad_words(first_name)
                middle_name = BannedWordsChecker.bad_words(middle_name)
                sur_name = BannedWordsChecker.bad_words(sur_name)

                # если false - проверка не пройдена
                if not first_name or not middle_name or not sur_name:
                    raise Exception("Inappropriate content")

            except Exception as err:

                if err == "Inappropriate content":
                    response.set_status(418)
                else:
                    response.set_status(417)

                return response.send()

            # проверка и запись пользователя
            try:
                if User.find_by_login(login):
                    response.set_status(409)
                    return response.send()

                # проверка иконки на наличие, валидность и "квадратность"
                if (pers_photo_data is not None) and (not is_image_valid(pers_photo_data) or not is_icon_square(pers_photo_data)):
                    response.set_status(420)
                    return response.send()

                unique_filename = generate_uuid()+".jpg"
                pers_photo_data = save_icon(pers_photo_data, unique_filename)  # сохранение иконки и возврат ее пути для записи

                # создание юзера в базе и выдача токена
                User.create_user(login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data)
                unique_token = generate_uuid()
                access_token = create_user_jwt_token(unique_token, login, password)

                response.set_data({
                    "session_token": access_token
                })

                return response.send()

            # если ошибка в логике сервера
            except Exception:
                response.set_status(504)
                return response.send()

        # логика авторизации
        elif action == 'LOGIN':
            try:
                login = data.get('login')
                password = data.get('password')

            except:
                response.set_status(417)
                return response.send()

            # проверка пользователя
            try:
                user = User.find_by_login(login)

            except Exception:
                response.set_status(504)
                return response.send()

            if user and user['password'] == password:
                unique_token = generate_uuid()
                access_token = create_user_jwt_token(unique_token, login, password)

                response.set_data({
                    "session_key": access_token
                })

                return response.send()

            else:
                response.set_status(417)
                return response.send()

        else:
            response.set_status(415)
            return response.send()

    # общая ошибка
    except Exception:
        response.set_status(400)
        return response.send()



# стандартные значения 
# могут быть не указаны limit = 5 page = 1 orderByDate=desc, search=''
# body = {
#     'filters': {
#         'orderByDate': 'desc',
#         'search' : '',
#     },
#     'limit': 5,
#     'page': 1,
#     'totalPosts': 100,
#     'posts': [],
# }


@api.route('/home', methods=['GET'])
def handle_posts():
    response = Response()
    
    # основной блок кода
    try:
        
        # получаем query string параметры для того, чтобы задать фильтры
        limit = request.args.get('limit')
        page = request.args.get('page')
        order = request.args.get('orderByDate')
        search = request.args.get('search')
        
        # получаем число постов в базе по заданному фильтру search
        posts_count = len(Post.get_all_posts(search=search))

        # если остальные параметры заданы кринжово, устанавливаем на дефолтные 
        # а может, эти проверки нужно вынести в Post.get_all_posts()?
        try:
            limit = int(limit)
            if limit > posts_count or limit < 1:
                if posts_count < 5:
                    limit = posts_count
                else:
                    limit = 5
        
        except:
            if posts_count < 5:
                limit = posts_count
            else:
                limit = 5
        

        try:
            page = int(page)
            if posts_count == limit or page > int(posts_count/limit) + 1 or page < 1:
                page = 1
        
        except:
            page = 1
        

        if order not in ['asc', 'desc']:
            order = 'desc'

        
        # пробуем получить и отправить посты
        try:
            posts = Post.get_all_posts(order, page, limit, search)
            response.set_data({
                'filters': {
                    'orderByDate': order,
                    'search' : search,
                },
                'limit': limit,
                'page': page,
                'totalPosts': posts_count,
                'posts': posts,
            })
            return response.send()
        
        except:
            response.set_status(504) # Database error
            return response.send()
            

    except:
        response.set_status(400) # Bad Request
        return response.send()


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

