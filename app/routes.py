from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, JWTManager, jwt_required, decode_token
from .database import *
from .generate_captcha import *
from .generate_token import *
from .validation_data import *
from .server_exception import Response
from dotenv import load_dotenv
from functools import wraps
import time
import os

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
TIME_CAPTCHA_LIMIT = int(os.getenv('CAPTCHA_EXPIRATION_MINUTES')) * 60  # в секундах
AUTHORIZATION_LIMIT = int(os.getenv('AUTHORIZATION_LIMIT')) * 60  # в секундах

api = Blueprint('api', __name__)  # добавляет api во всех раутах
jwt = JWTManager()  # объект генерации токенов


## ЗАДАЧИ:

# сделать новую логику некоторых методов и протестить их (они не работают щас блять!)
# сделать логику модераторов (полномочия без огрничений, кроме удаления других модераторов)
# сделать методы удаления чужих постов и "бана по ip"  ??

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
            identity = get_jwt_identity()  # получение токена авторизации
            owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)
            password = encrypt_decrypt(identity["password"], SECRET_KEY)

            user = User.find_by_login(owner_login)

            # проверка логина и пароля пользователя
            if not user or password != user[1]:
                response.set_status(410)
                return response.send()

        # если ошибка декодирования
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
    captcha_created_time = int(time.time())  # время, до которого капча валидна
    token = create_access_token(identity={"solution": encoded_captcha_solution, "created_time": captcha_created_time})

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

        if action != "REGISTER" and action != "LOGIN":
            response.set_status(415)
            return response.send()

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
            captcha_created_time = decoded_captcha_token['sub']['created_time']

        except:
            response.set_status(413)
            return response.send()

        current_time = int(time.time())  # в секундах

        # проверка актуального времени капчи
        # if captcha_created_time + TIME_CAPTCHA_LIMIT < current_time:
        #     response.set_status(416)
        #     return response.send()

        # проверка пользовательского решения капчи
        if input_captcha != captcha_solution:
            response.set_status(414)
            return response.send()

        # поля для обоих сценариев
        login = data.get('login')
        password = data.get('password')

        # логика регистрации
        if action == 'REGISTER':
            try:
                # публичные поля (требуют проверки на badwords)
                first_name = data.get('first_name')
                middle_name = data.get('middle_name')
                sur_name = data.get('sur_name')

                # непубличные поля (не требуют проверки на badwords)
                email = data.get('email')
                phone_number = data.get('phone_number')
                pers_photo_data = data.get('pers_photo_data')

                # валидация всех полей
                is_valid, validation_error = check_user_data(data)
                if not is_valid:
                    response.set_status(417)
                    response.set_message(validation_error)
                    return response.send()

                # проверка на плохие слова
                if not check_bad_words(first_name, middle_name, sur_name):
                    response.set_status(418)
                    return response.send()

                header, pers_photo_data = pers_photo_data.split(",", 1)

                if pers_photo_data is not None:
                     # проверка иконки на наличие, валидность и "квадратность"
                    if not is_image_valid(pers_photo_data) or not is_icon_square(pers_photo_data):
                        response.set_status(420)
                        return response.send()

                    # сохранение иконки и возврат ее пути для записи
                    unique_filename = generate_uuid() + ".png"
                    pers_photo_data = save_icon(pers_photo_data, unique_filename)

            # если данные некорректны
            except Exception:
                response.set_status(417)
                return response.send()

            # проверка и запись пользователя
            try:
                if User.find_by_login(login):
                    response.set_status(409)
                    return response.send()

                # создание юзера в базе и выдача токена
                User.create_user(login, password, first_name, middle_name, sur_name, email, phone_number, pers_photo_data)

            # если ошибка в логике сервера
            except Exception:
                response.set_status(504)
                return response.send()

        # логика авторизации
        if action == 'LOGIN':
            # проверка пользователя
            try:
                user = User.find_by_login(login)

            # если ошибка в логике сервера
            except Exception:
                response.set_status(504)
                return response.send()

            if not user or user[1] != password:
                response.set_status(417)
                return response.send()

        # кодируем логин и пароль
        encoded_login = encrypt_decrypt(login, SECRET_KEY)
        encoded_password = encrypt_decrypt(password, SECRET_KEY)

        # в любом случае возвращаем токен
        access_token = create_user_jwt_token(encoded_login, encoded_password)

        response.set_data({
            "session_token": access_token
        })

        return response.send()

    # общая ошибка
    except Exception:
        response.set_status(400)
        return response.send()


@api.route('/home', methods=['GET'])  # метод получения всех постов  !!!
def handle_posts():
    response = Response()

    try:
        # получаем query string параметры
        limit = request.args.get('limit', default=5)
        page = request.args.get('page', default=1)
        order = request.args.get('orderByDate', default='desc')
        search = request.args.get('search', default='')

        # получаем число постов по заданному фильтру search
        posts_count = len(Post.get_all_posts(search=search))

        # корректные преобразования значений запроса
        try:
            page, limit = int(page), int(limit)
        except ValueError:
            page, limit = 1, 5

        limit = min(max(limit, 1), min(posts_count, 5))

        max_page = (posts_count - 1) // limit + 1
        page = min(max(page, 1), max_page)

        if order not in ['asc', 'desc']:
            order = 'desc'

        # получение постов по запросу
        try:
            posts = Post.get_all_posts(order, page, limit, search)
            response.set_data({
                'filters': {
                    'orderByDate': order,
                    'search': search,
                },
                # 'operations': {
                #     'delete': endpoint удаления постов
                #
                # },
                'limit': limit,
                'page': page,
                'totalPosts': posts_count,
                'posts': posts,
            })
            return response.send()

        # если ошибка в логике сервера
        except:
            response.set_status(504)
            return response.send()

    # общая ошибка
    except:
        response.set_status(400)
        return response.send()


@api.route('/<post_id>', methods=['GET'])  # метод получения одного поста(с обновлением просмотровБ лайков и дизлайков) ???
def hadle_post(post_id):
    pass


@api.route('/create_post', methods=['POST'])  # метод создания нового поста
@jwt_required()
def create_post():
    response = Response()

    data = request.get_json()

    # получение и обработка данных
    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags")
        image_data = data.get("image_data")

        # валидация всех полей
        is_valid, validation_error = check_post_data(data)
        if not is_valid:
            response.set_status(417)
            response.set_message(validation_error)
            return response.send()

        # проверка на плохие слова
        if not check_bad_words(title, content, tags):
            response.set_status(418)
            return response.send()

    # если данные некорректны
    except Exception:
        response.set_status(417)
        return response.send()

    # запись нового поста
    try:
        if image_data is not None:
            header, image_data = image_data.split(",", 1)

            # проверка иконки на наличие и валидность
            if not is_image_valid(image_data) or not check_image_aspect_ratio(image_data):
                response.set_status(420)
                return response.send()

            # сохранение иконки и возврат ее пути для записи
            unique_filename = generate_uuid() + ".png"
            image_data = save_image(image_data, unique_filename)

        unique_id = generate_uuid()
        Post.create_post(unique_id, owner_login, title, content, tags, image_data)

        return response.send()

    # если ошибка в логике сервера
    except Exception as e:
        print(e)
        response.set_status(504)
        return response.send()


@api.route('/post/edit_post', methods=['PUT', 'DELETE'])  # метод редактирования и/или удаления поста  !!!
@jwt_required()
def edit_post():
    response = Response()

    action = request.headers.get('Target-Action')

    if action != "UPDATE" and action != "DELETE":
        response.set_status(415)
        return response.send()

    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        data = request.get_json()
        unique_id = data["unique_id"]

        if not Post.get_post_by_id(unique_id):
            response.set_status(419)
            return response.send()

    except Exception:
        response.set_status(417)
        return response.send()

    if action == "UPDATE" and request.method == 'PUT':
        try:
            title = data.get("title")
            content = data.get("content")
            tags = data.get("tags")
            image_data = data.get("image_data")

            # валидация полей
            is_valid, validation_error = check_post_data(data)
            if not is_valid:
                response.set_status(417)
                response.set_message(validation_error)
                return response.send()

            # проверка на плохие слова
            if not check_bad_words(title, content, tags):
                response.set_status(418)
                return response.send()

            if image_data is not None:
                # проверка иконки на наличие и валидность
                if not is_image_valid(image_data) or not check_image_aspect_ratio(image_data):
                    response.set_status(420)
                    return response.send()

                # сохранение иконки и возврат ее пути для записи
                header, image_data = image_data.split(",", 1)
                unique_filename = generate_uuid() + ".jpg"
                image_data = save_image(image_data, unique_filename)

        except Exception:
            response.set_status(417)
            return response.send()

        # обновляем пост в базе
        try:
            Post.update_post(unique_id, owner_login, title=title, content=content, tags=tags, image_data=image_data)

        # если ошибка в логике сервера
        except Exception:
            response.set_status(504)
            return response.send()

        response.set_status(205)
        return response.send()

    if action == "DELETE" and request.method == 'DELETE':
        try:
            Post.delete_post(unique_id, owner_login=owner_login)

        # если ошибка в логике сервера
        except Exception:
            response.set_status(504)
            return response.send()

        response.set_status(206)
        return response.send()


@api.route('<int:post_id>/comments', methods=['GET'])  # метод получения комменнтов к посту  ??? tests
def handle_comments(post_id):
    response = Response()

    try:
        all_posts = Post.get_all_posts()
        posts_id = [post[0] for post in all_posts]

        # если пост с таким id существует
        if post_id in posts_id:

            comments_count = len(Comment.get_comments_by_post(post_id))

            # получаем query string параметры
            limit = request.args.get('limit', default=5)
            page = request.args.get('page', default=1)
            order = request.args.get('orderByDate', default='desc')

            # корректные преобразования значений запроса
            try:
                page, limit = int(page), int(limit)
            except ValueError:
                page, limit = 1, 5

            if 1 > limit or comments_count < limit:
                limit = min(comments_count, 5)

            # формула максимально возможной страницы с данным лимитом и кол-вом постов
            try:
                max_page = (comments_count - 1) // limit + 1
            # если постов нет, нет и limit, но одну страницу мы отобразить должны
            except ZeroDivisionError:
                max_page = 1

            # проверяем page на допустимый диапазон
            if page < 1 or page > max_page:
                page = 1

            if order not in ['asc', 'desc']:
                order = 'desc'

            # пытаемся получить комментарии к посту
            try:
                comments = Comment.get_comments_by_post(post_id, order, page, limit)
                response.set_data({
                    'filters': {
                        'orderByDate': order
                    },
                    'limit': limit,
                    'page': page,
                    'totalComments': comments_count,
                    'comments': comments,
                })

                return response.send()

            # если ошибка в логике сервера
            except:
                response.set_status(504)
                return response.send()

        # ошибка "не найдено"
        else:
            response.set_status(404)
            return response.send()

    # общая ошибка
    except:
        response.set_status(400)
        return response.send()

@api.route('/<post_id>/add_comment', methods=['POST'])  # метод создания коммента
@jwt_required()
def create_comment(post_id):
    response = Response()

    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        # Извлечение полей из данных запроса
        data = request.get_json()
        content = data.get('content')

        # Валидация данных комментария
        is_valid, validation_error = check_comment_data(data)

        if not is_valid:
            response.set_status(417)
            response.set_message(validation_error)
            return response.send()

        # Проверка на наличие неприемлемого контента с помощью проверки плохих слов
        if not check_bad_words(content):
            response.set_status(418)
            return response.send()
    except:
        response.set_status(417)
        return response.send()

    try:
        unique_id = generate_uuid()
        # Создание комментария в базе данных
        Comment.create_comment(unique_id, owner_login, post_id, content)

    except Exception:
        response.set_status(504)
        return response.send()

    response.set_status(201)
    return response.send()


@api.route('/post/comment/<int:id>/', methods=['PUT', 'DELETE'])  # метод редактирования и/или удаления коммента  !!!
@jwt_required()
def edit_comment():
    response = Response()

    action = request.headers.get('Target-Action')

    if action != "UPDATE" and action != "DELETE":
        response.set_status(415)
        return response.send()

    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        data = request.get_json()
        unique_id = data["unique_id"]

        if not Post.get_post_by_id(unique_id):
            response.set_status(419)
            return response.send()

    except Exception:
        response.set_status(417)
        return response.send()

    if action == "UPDATE" and request.method == 'PUT':
        try:
            content = data.get("content")

            is_valid, validation_error = check_comment_data(data)

            if not is_valid:
                response.set_status(417)
                response.set_message(validation_error)
                return response.send()

            if not check_bad_words(content):
                response.set_status(418)
                return response.send()

        except Exception:
            response.set_status(417)
            return response.send()

        try:
            Comment.update_comment(unique_id, owner_login, content)
            response.set_status(205)

        except Exception:
            response.set_status(504)
            return response.send()

    if action == "DELETE" and request.method == 'DELETE':
        try:
            Comment.delete_comment(unique_id, owner_login)
            response.set_status(206)

        except Exception:
            response.set_status(504)

    return response.send()



@api.route('/edit_user', methods=['PUT'])  # метод редактирования данных пользователя  ---
def edit_userprofile():
    pass






