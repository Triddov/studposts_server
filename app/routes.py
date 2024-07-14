from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required
from functools import wraps
from .database import User, Post, Comment
from .generate_captcha import generate_captcha, generate_captcha_image


api = Blueprint('api', __name__)
jwt = JWTManager()  # объект генерации токенов

# Первоочередное:
# сделать отдельный get эндпоинт (/capcha/) для капчи

# генерировать названия постов, картинок и ключей (использовать sha256 для ключей)
# проверять данные юзера, постов, комментов и (главное блять) фоток (это фото, размер, квадратное)
# волюм для sourses и json названий


@api.route('/captcha', methods=['GET'])
def get_captcha():
    captcha_text = generate_captcha()
    base64_image = generate_captcha_image(captcha_text)
    token = create_access_token(identity={'captcha': captcha_text})
    return jsonify({
        'captcha_image': base64_image,  # изображение капчи, закодированное в base64
        'token': token  # решение капчи, закодированное как jwt-токен
    })


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({"msg": "Token is missing"}), 401  # ошибка авторизации

        try:
            get_jwt_identity()  # будет ошибка, если токен недействителен
        except:
            return jsonify({"msg": "Token is invalid"}), 401  # ошибка авторизации
        return f(*args, **kwargs)
    return decorator


@api.route('/auth/', methods=['POST'])
def auth():
    action = request.headers.get('Target-Action')

    data = request.get_json()

    if action == 'REGISTER': # чекнуть форму
        login = data.get('login')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        pers_photo_data = data.get('pers_photo_data')

        if User.find_by_login(login):
            return jsonify({"msg": "User already exists"}), 400  # некорректный запрос

        user_login = User.create_user(login, username, password, first_name, last_name, email, phone_number, pers_photo_data)
        return jsonify({"msg": "User registered successfully", "user_login": user_login}), 201  # успешное создание

    elif action == 'LOGIN':
        login = data.get('login')
        password = data.get('password')
        user = User.find_by_login(login)

        if user and user['password'] == password:
            access_token = create_access_token(identity=user['login'])
            return jsonify(access_token=access_token), 200  # успешно

        else:
            return jsonify({"msg": "Invalid credentials"}), 401  # ошибка авторизации
    else:
        return jsonify({"msg": "No action specified"}), 400  # некорректный запрос


@api.route('/posts/', methods=['GET'])
@token_required
def handle_posts():
    sort = request.args.get('sort', 'date')
    order = request.args.get('order', 'desc')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    posts = Post.get_all_posts(sort, order, page, limit)
    return jsonify(posts), 200  # успешно


@api.route('/post/create/', methods=['POST'])
@token_required
def new_post():
    user_login = get_jwt_identity()

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags')
    image_data = data.get('image_data')

    post_id = Post.create_post(user_login, title, content, tags, image_data)
    return jsonify({"msg": "Post created successfully", "post_id": post_id}), 201  # успешное создание


@api.route('/post/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_post(id):
    post = Post.get_post_by_id(id)
    user_login = get_jwt_identity()

    if not post:
        return jsonify({"msg": "Post not found"}), 404  # не найдено

    if request.method == 'GET':
        return jsonify(post), 200  # успешно

    if post['user_login'] != user_login:
        return jsonify({"msg": "Permission denied"}), 403  # нет прав доступа

    if request.method == 'PUT':
        data = request.get_json()
        title = data.get('title', post['title'])
        content = data.get('content', post['content'])
        tags = data.get('tags', post['tags'])
        image_data = data.get('image_data', post['imageData'])
        Post.update_post(id, title, content, tags, image_data)
        return jsonify({"msg": "Post updated successfully"}), 200  # успешно

    if request.method == 'DELETE':
        Post.delete_post(id)
        return jsonify({"msg": "Post deleted successfully"}), 204  # успешно


@api.route('/post/<int:post_id>/comments/', methods=['GET'])
@token_required
def handle_comments(post_id):
    if request.method == 'GET':
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        comments = Comment.get_comments_by_post(post_id, sort, order, page, limit)
        return jsonify(comments), 200  # успешно


@api.route('/post/<int:post_id>/comment/create/', methods=['POST'])
@token_required
def new_comment():
    data = request.get_json()
    content = data.get('content')
    image_data = data.get('image_data')
    tags = data.get('tags')
    post_id = data.get('post_id')
    user_login = get_jwt_identity()

    comment_id = Comment.create_comment(user_login, post_id, content, image_data, tags)
    return jsonify({"msg": "Comment created successfully", "comment_id": comment_id}), 201  # успешное создание


@api.route('/post/<int:post_id>/comment/<int:id>/', methods=['PUT', 'DELETE'])
@token_required
def handle_comment(id):
    user_login = get_jwt_identity()
    comment = Comment.get_comment_by_id(id)

    if not comment:
        return jsonify({"msg": "Comment not found"}), 404  # не найдено

    if comment['user_login'] != user_login:
        return jsonify(
            {"msg": "Permission denied"}), 403  # нет прав доступа

    if request.method == 'PUT':
        data = request.get_json()
        content = data.get('content')
        image_data = data.get('image_data')
        tags = data.get('tags')
        Comment.update_comment(id, content, image_data, tags)
        return jsonify({"msg": "Comment updated successfully"}), 200  # успешно

    if request.method == 'DELETE':
        Comment.delete_comment(id)
        return jsonify({"msg": "Comment deleted successfully"}), 204  # успешное удаление


@api.route('/posts/<int:post_id>/view', methods=['PUT'])
@token_required
def update_view_count(post_id):
    try:
        Post.increment_view(post_id)
        return jsonify({'message': 'View count incremented successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # ошибка сервера


@api.route('/posts/<int:post_id>/like', methods=['PUT'])
@token_required
def update_likes_count(post_id):
    try:
        Post.like_post(post_id)
        return jsonify({'message': 'Likes count incremented successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # ошибка сервера


@api.route('/posts/<int:post_id>/dislike', methods=['PUT'])
@token_required
def update_dislikes_count(post_id):
    try:
        Post.dislike_post(post_id)
        return jsonify({'message': 'Dislikes count incremented successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # ошибка сервера
