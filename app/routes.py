from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import get_jwt_identity, JWTManager, jwt_required, decode_token
from .database import *
from .generate_captcha import *
from .generate_token import *
from .validation_data import *
from .server_exception import Response, log_status
from dotenv import load_dotenv
from functools import wraps
import time
import os

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
TIME_CAPTCHA_LIMIT = int(os.getenv('CAPTCHA_EXPIRATION_MINUTES')) * 60  # в секундах
AUTHORIZATION_LIMIT = int(os.getenv('AUTHORIZATION_LIMIT')) * 60  # в секундах

nginx_blacklist_path = 'nginx_blacklist.conf'  # путь из корня проекта к списку забаненных по ip
nginx_banned_ips = load_nginx_blacklist(nginx_blacklist_path)

api = Blueprint('api', __name__)  # добавляет api во всех раутах
jwt = JWTManager()  # объект генерации токенов


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
            if not user or password != user['password']:
                response.set_status(410)
                return response.send()

        # если ошибка декодирования
        except Exception as err:
            log_status(err, __name__)
            response.set_status(406)
            return response.send()

        return f(*args, **kwargs)

    return decorator


@api.before_request
def check_ban_ip():
    response = Response()

    ip = request.remote_addr
    if ip in nginx_banned_ips:
        response.set_status(403)  # abort(403)
        return response.send()


@api.route('/ban_ip', methods=['POST'])
def ban_ip():
    response = Response()

    ip_address = request.form.get('ip_address')
    if ip_address:
        with open(nginx_blacklist_path, 'a') as ban_list:
            ban_list.write(f"deny {ip_address};\n")

        nginx_banned_ips.add(ip_address)
        response.set_message(f"IP {ip_address} has been banned")
        return response.send()

    response.set_status(400)
    response.set_message("Invalid IP address")
    return response.send()


@api.route('/sources/<path:filename>', methods=["GET"])
def serve_resources(filename):
    return send_from_directory('../sources', filename)


@api.route('/captcha', methods=['GET'])  # метод генерации и получения капчи
def get_captcha():
    response = Response()

    # генерация капчи
    captcha_text = generate_captcha()
    encoded_captcha_solution = encrypt_decrypt(captcha_text, SECRET_KEY)
    base64_image = generate_captcha_image(captcha_text)
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

        except Exception as err:
            log_status(err, __name__)
            response.set_status(413)
            return response.send()

        current_time = int(time.time())  # в секундах

        # проверка актуального времени капчи
        if captcha_created_time + TIME_CAPTCHA_LIMIT < current_time:
            response.set_status(416)
            return response.send()

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

                if pers_photo_data is not None:
                    header, pers_photo_data = pers_photo_data.split(",", 1)

                    # проверка иконки на наличие, валидность и "квадратность"
                    if not is_image_valid(pers_photo_data):
                        response.set_status(420)
                        return response.send()

                    if not is_icon_square(pers_photo_data):
                        pers_photo_data = crop_to_square(pers_photo_data)

            # если данные некорректны
            except Exception as err:
                log_status(err, __name__)
                response.set_status(417)
                return response.send()

            # проверка и запись пользователя
            try:
                if User.find_by_login(login):
                    response.set_status(409)
                    return response.send()

                # сохранение иконки и возврат ее пути для записи
                if pers_photo_data is not None:
                    unique_filename = generate_uuid() + ".png"
                    pers_photo_data = save_icon(pers_photo_data, unique_filename)
                else:
                    pers_photo_data = "sources/userProfileIcons/default_user_icon.png"

                # создание юзера в базе и выдача токена
                User.create_user(login, password, first_name, sur_name, middle_name, email, phone_number,
                                 pers_photo_data)

            # если ошибка в логике сервера
            except Exception as err:
                log_status(err, __name__)
                response.set_status(504)
                return response.send()

        # логика авторизации
        if action == 'LOGIN':
            # проверка пользователя
            try:
                user_data = User.find_by_login(login)

            # если ошибка в логике сервера
            except Exception as err:
                log_status(err, __name__)
                response.set_status(504)
                return response.send()

            if not user_data or user_data['password'] != password:
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
    except Exception as err:
        log_status(err, __name__)
        response.set_status(400)
        return response.send()


@api.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    response = Response()
    identity = get_jwt_identity()
    login = encrypt_decrypt(identity["login"], SECRET_KEY)

    try:
        user_data = User.get_user(login)
        response.set_data({"user_data": user_data})
        return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(404)
        return response.send()


@api.route('/home', methods=['GET'])  # метод получения всех постов
@jwt_required(True)
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
        except ValueError as err:
            log_status(err, __name__)
            page, limit = 1, 5

        # если limit вне диапазона количества постов
        if 1 > limit or posts_count < limit:
            # то он равен либо 5, либо количеству постов, если оно меньше 5 (например если постов 4, то limit=4, а не 5)
            limit = min(posts_count, 5)

        # формула максимально возможной страницы с данным лимитом и кол-вом постов
        try:
            max_page = (posts_count - 1) // limit + 1

        # если постов нет, нет и limit, но одну страницу мы отобразить должны
        except ZeroDivisionError as err:
            log_status(err, __name__)
            max_page = 1

        # проверяем page на допустимый диапазон
        if page < 1 or page > max_page:
            page = 1

        if order not in ['asc', 'desc']:
            order = 'desc'

        # получение постов по запросу
        try:
            posts = Post.get_all_posts(order, page, limit, search)

            # проверка, авторизован ли пользователь и какие у него доступны операции
            try:
                identity = get_jwt_identity()
                login = encrypt_decrypt(identity["login"], SECRET_KEY)

                # модифицируем операции в зависимости от роли пользователя
                for post in posts:
                    # если он создатель
                    if post['owner_login'] == login:
                        post['operations'] = {
                            'delete': f'/api/{post['unique_id']}/delete',
                            'update': f'/api/{post['unique_id']}/update'
                        }

                    # если он модератор и это не пост другого модератора
                    elif (User.is_moderator(login)) and (not User.is_moderator(post['owner_login'])):
                        post['operations'] = {
                            'delete': f'/api/{post['unique_id']}/delete',
                            'ban': f'/api/ban_ip'
                        }

                    post['reaction'] = User.get_reaction_at_post(login, post['unique_id'])

            except Exception as err:
                log_status(err, __name__)

            response.set_data({
                'filters': {
                    'orderByDate': order,
                    'search': search,
                },
                'limit': limit,
                'page': page,
                'totalPosts': posts_count,
                'posts': posts,
            })

            return response.send()

        # если ошибка в логике сервера
        except Exception as err:
            log_status(err, __name__)
            response.set_status(504)
            return response.send()

    # общая ошибка
    except Exception as err:
        log_status(err, __name__)
        response.set_status(400)
        return response.send()


@api.route('/<post_id>', methods=['GET'])  # метод получения одного поста(с обновлением просмотров)
@jwt_required(True)
def handle_post(post_id):
    response = Response()

    try:
        Post.increment_view(post_id)
        post = Post.get_post_by_id(post_id)

        # проверка, авторизован ли пользователь и какие у него доступны операции
        try:
            identity = get_jwt_identity()
            login = encrypt_decrypt(identity["login"], SECRET_KEY)

            # модифицируем операции в зависимости от роли пользователя
            if post['owner_login'] == login:
                post['operations'] = {
                    'delete': f'/api/{post['unique_id']}/delete',
                    'update': f'/api/{post['unique_id']}/update'
                }

            # если он модератор и это не пост другого модератора
            elif (User.is_moderator(login)) and (not User.is_moderator(post['owner_login'])):
                post['operations'] = {
                    'delete': f'/api/{post['unique_id']}/delete',
                    'ban': f'/api/ban_ip'
                }

            # добавляем поле с реакцией пользователя на пост
            post['reaction'] = User.get_reaction_at_post(login, post['unique_id'])

        except Exception as err:
            log_status(err, __name__)

        response.set_data({
            'post': post
        })
        return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(504)


@api.route('/home/create_post', methods=['POST'])  # метод создания нового поста
@jwt_required()
def create_post():
    response = Response()

    # получение и обработка данных
    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        data = request.get_json()

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
    except Exception as err:
        log_status(err, __name__)
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
    except Exception as err:
        log_status(err, __name__)
        response.set_status(421)
        return response.send()


@api.route('/<post_id>/update', methods=['PUT'])  # метод редактирования поста
@jwt_required()
def update_post(post_id):
    response = Response()
    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        if not Post.get_post_by_id(post_id):
            response.set_status(419)
            return response.send()

        data = request.get_json()
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
            header, image_data = image_data.split(",", 1)

            # проверка иконки на наличие и валидность
            if not is_image_valid(image_data) or not check_image_aspect_ratio(image_data):
                response.set_status(420)
                return response.send()
            # сохранение изображения и возврат его пути для записи(или перезаписи, если она есть уже)
            if Post.image_already(post_id):
                unique_filename = Post.image_filename(post_id)
                os.remove("sources/userPostImages/" + unique_filename)
            else:
                unique_filename = generate_uuid() + ".png"

            image_data = save_image(image_data, unique_filename)

    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()

    # обновляем пост в базе
    try:
        Post.update_post(post_id, owner_login, title=title, content=content, tags=tags, imagedata=image_data)
        response.set_status(205)
        return response.send()

    # если ошибка в логике сервера
    except Exception as err:
        log_status(err, __name__)
        response.set_status(504)
        return response.send()


@api.route('/<post_id>/delete/', methods=['DELETE'])  # метод удаления поста
@jwt_required()
def delete_post(post_id):
    response = Response()

    try:
        jwt_identity = get_jwt_identity()
        owner_login = encrypt_decrypt(jwt_identity["login"], SECRET_KEY)

    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()

    try:
        Post.delete_post(post_id, owner_login=owner_login)
        response.set_status(206)
        return response.send()

    # если ошибка в логике сервера
    except Exception as err:
        log_status(err, __name__)
        response.set_status(504)
        return response.send()


@api.route('<post_id>/comments', methods=['GET'])  # метод получения комментов к посту
@jwt_required(True)
def handle_comments(post_id):
    response = Response()

    try:
        all_posts = Post.get_all_posts()
        posts_id = [post['unique_id'] for post in all_posts]

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
            except ValueError as err:
                log_status(err, __name__)
                page, limit = 1, 5

            if 1 > limit or comments_count < limit:
                limit = min(comments_count, 5)

            # формула максимально возможной страницы с данным лимитом и кол-вом постов
            try:
                max_page = (comments_count - 1) // limit + 1
            # если постов нет, нет и limit, но одну страницу мы отобразить должны
            except ZeroDivisionError as err:
                log_status(err, __name__)
                max_page = 1

            # проверяем page на допустимый диапазон
            if page < 1 or page > max_page:
                page = 1

            if order not in ['asc', 'desc']:
                order = 'desc'

            # пытаемся получить комментарии к посту
            try:
                comments = Comment.get_comments_by_post(post_id, order, page, limit)

                # проверка, авторизован ли пользователь и какие у него доступны операции
                try:
                    identity = get_jwt_identity()
                    login = encrypt_decrypt(identity["login"], SECRET_KEY)

                    for comment in comments:
                        # модифицируем операции в зависимости от роли пользователя
                        if comment['owner_login'] == login:
                            comment['operations'] = {
                                'delete': f'/api/{comment['post_id']}/delete_comment',
                                'update': f'/api/{comment['post_id']}/update_comment'
                            }

                        # если он модератор и это не пост другого модератора
                        elif (User.is_moderator(login)) and (not User.is_moderator(comment['owner_login'])):
                            comment['operations'] = {
                                'delete': f'/api/{comment['post_id']}/delete_comment',
                                'ban': f'/api/ban_ip'
                            }

                except Exception as err:
                    log_status(err, __name__)

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
            except Exception as err:
                log_status(err, __name__)
                response.set_status(504)
                return response.send()

        # ошибка "не найдено"
        else:
            response.set_status(404)
            return response.send()

    # общая ошибка
    except Exception as err:
        log_status(err, __name__)
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
    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()

    try:
        unique_id = generate_uuid()
        # Создание комментария в базе данных
        Comment.create_comment(unique_id, owner_login, post_id, content)

    except Exception as err:
        log_status(err, __name__)
        response.set_status(504)
        return response.send()

    response.set_status(201)
    return response.send()


@api.route('/<post_id>/update_comment', methods=['PUT'])  # метод редактирования коммента
@jwt_required()
def update_comment(post_id):
    response = Response()

    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        data = request.get_json()
        content = data.get("content")
        comment_id = data.get("comment_id")

        if not Post.get_post_by_id(post_id) or not Comment.get_comment_by_id(comment_id):
            response.set_status(419)
            return response.send()

        is_valid, validation_error = check_comment_data(data)

        if not is_valid:
            response.set_status(417)
            response.set_message(validation_error)
            return response.send()

        if not check_bad_words(content):
            response.set_status(418)
            return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()

    try:
        Comment.update_comment(comment_id, owner_login, content)
        response.set_status(205)
        return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(421)
        return response.send()


@api.route('/<post_id>/delete_comment', methods=['DELETE'])  # метод удаления коммента
@jwt_required()
def delete_comment(post_id):
    response = Response()

    data = request.get_json()
    comment_id = data.get("comment_id")

    try:
        identity = get_jwt_identity()
        owner_login = encrypt_decrypt(identity["login"], SECRET_KEY)

        if not Post.get_post_by_id(post_id) or not Comment.get_comment_by_id(comment_id):
            response.set_status(419)
            return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()

    try:
        Comment.delete_comment(comment_id, owner_login)
        response.set_status(206)
        return response.send()

    except Exception as err:
        log_status(err, __name__)
        response.set_status(421)


@api.route('/edit_user', methods=['PUT'])  # метод редактирования данных пользователя
@jwt_required()
def edit_userprofile():
    response = Response()
    encoded_password, access_token = None, None  # заготовки для будущего токена

    try:
        identity = get_jwt_identity()
        original_login = encrypt_decrypt(identity["login"], SECRET_KEY)
        original_password = encrypt_decrypt(identity["password"], SECRET_KEY)

        # Получение данных из запроса
        data = request.get_json()
        password = data.get("password")
        first_name = data.get("first_name")
        middle_name = data.get("middle_name")
        sur_name = data.get("sur_name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        pers_photo_data = data.get("pers_photo_data")

        # проверка на соответствие пароля
        current_password = data.get('current_password')
        if current_password != original_password:
            response.set_status(410)
            return response.send()

        # Валидация данных пользователя
        is_valid, validation_error = check_user_data(data, 'update')
        if not is_valid:
            response.set_status(417)
            response.set_message(validation_error)
            return response.send()

        # Проверка на наличие недопустимых слов в именах пользователя
        if not check_bad_words(first_name, middle_name, sur_name):
            response.set_status(418)
            return response.send()

        # Обработка данных о персональном фото

        # кейс сброса изображения до дефолтного
        if pers_photo_data is None or pers_photo_data == "":
            pers_photo_data = "sources/userProfileIcons/default_user_icon.png"

        # кейс других данных
        elif pers_photo_data is not None:
            header, pers_photo_data = pers_photo_data.split(",", 1)

            if not is_image_valid(pers_photo_data) or not is_icon_square(pers_photo_data):
                response.set_status(420)
                return response.send()
            unique_filename = generate_uuid() + ".png"
            pers_photo_data = save_icon(pers_photo_data, unique_filename)

    except Exception as err:
        log_status(err, __name__)

        response.set_status(417)
        return response.send()

    try:
        # Обновление данных пользователя в базе данных
        User.update_user(original_login, password, first_name, middle_name, sur_name, email, phone_number,
                         pers_photo_data)

        try:
            # создание нового токена при изменении пароля
            if password:
                encoded_password = encrypt_decrypt(password, SECRET_KEY)
                access_token = create_user_jwt_token(original_login, encoded_password)

            response.set_status(205)
            if access_token:
                response.set_data(({
                    "session_token": access_token
                }))
            return response.send()

        except Exception as err:
            log_status(err, __name__)
            response.set_status(405)
            return response.send()

    # данных не поступило
    except Exception as err:
        log_status(err, __name__)
        response.set_status(417)
        return response.send()


@api.route('/<post_id>/rate/', methods=['PUT'])  # метод лайков/дизлайков под постом
@jwt_required()
def rate(post_id):
    response = Response()

    try:
        identity = get_jwt_identity()
        login = encrypt_decrypt(identity["login"], SECRET_KEY)

        all_posts = Post.get_all_posts()
        posts_id = [post['unique_id'] for post in all_posts]

        # если пост с таким id существует
        if post_id in posts_id:

            data = request.get_json()
            action = data.get('action')

            try:
                # перебор доступных action
                if action in ['like', 'dislike', 'none']:
                    Post.rate_post(login, post_id, action)

                # неизвестное действие
                else:
                    response.set_status(412)
                    return response.send()

                response.set_status(200)
                return response.send()

            except Exception as err:
                log_status(err, __name__)
                response.set_status(504)
                return response.send()

        # ошибка "не найдено"
        else:
            response.set_status(404)
            return response.send()

    # общая ошибка
    except Exception as err:
        log_status(err, __name__)
        response.set_status(400)
        return response.send()


@api.route('/<post_id>/get_rates', methods=['GET'])
@jwt_required()
def get_rates(post_id):
    response = Response()
    post = Post.get_post_by_id(post_id)

    identity = get_jwt_identity()
    login = encrypt_decrypt(identity["login"], SECRET_KEY)

    likes_count, dislikes_count = Rate.get_rate(post_id)
    reaction = User.get_reaction_at_post(login, post["unique_id"])
    response.set_data({"likes_count": likes_count,
                       "dislikes_count": dislikes_count,
                       "reaction": reaction})
    return response.send()
