from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager
from functools import wraps
from .database import User, Post, Comment

api = Blueprint('api', __name__)
jwt = JWTManager()  # объект генерации токенов

# Первоочередное:
# сделать отдельный get эндпоинт (/capcha/) для капчи
# генерировать названия картинок и ключей (использовать sha256 для ключей)
# проверять данные юзера, постов, комментов и (главное блять) фоток
# + лайки


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
    action = request.headers.get('TARGET_ACTION')
    if not action:
        return jsonify({"msg": "No action specified"}), 400  # некорректный запрос

    data = request.get_json()

    if action == 'REGISTER':
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        pers_photo_data = data.get('pers_photo_data')

        if User.find_by_email(email):
            return jsonify({"msg": "User already exists"}), 400  # некорректный запрос

        user_id = User.create_user(username, password, first_name, last_name, email, phone_number, pers_photo_data)
        return jsonify({"msg": "User registered successfully", "user_id": user_id}), 201 # успешное создание

    elif action == 'LOGIN':
        email = data.get('email')
        password = data.get('password')
        user = User.find_by_email(email)

        if user and user['password'] == password:
            access_token = create_access_token(identity=user['id'])
            return jsonify(access_token=access_token), 200  # успешно

        else:
            return jsonify({"msg": "Invalid credentials"}), 401  # ошибка авторизации
    else:
        return jsonify({"msg": "Invalid action"}), 400  # некорректный запрос


@api.route('/posts/', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        posts = Post.get_all_posts(sort, order, page, limit)
        return jsonify(posts), 200  # успешно

    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')
        image_data = data.get('image_data')
        user_id = get_jwt_identity()

        post_id = Post.create_post(user_id, title, content, tags, image_data)
        return jsonify({"msg": "Post created successfully", "post_id": post_id}), 201  # успешное создание


@api.route('/posts/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_post(id):
    post = Post.get_post_by_id(id)

    if request.method == 'GET':
        return jsonify(post), 200  # успешно

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
        return jsonify({"msg": "Post deleted successfully"}), 204  # успешное удаление


@api.route('/posts/<int:post_id>/comments/', methods=['GET', 'POST'])
@token_required
def handle_comments(post_id):
    if request.method == 'GET':
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        comments = Comment.get_comments_by_post(post_id, sort, order, page, limit)
        return jsonify(comments), 200  # успешно

    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        image_data = data.get('image_data')
        tags = data.get('tags')
        user_id = get_jwt_identity()

        comment_id = Comment.create_comment(user_id, post_id, content, image_data, tags)
        return jsonify({"msg": "Comment created successfully", "comment_id": comment_id}), 201  # успешное создание


@api.route('/comments/<int:id>/', methods=['PUT', 'DELETE'])
@token_required
def handle_comment(id):
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
