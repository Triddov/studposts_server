from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, Post, Comment

api = Blueprint('api', __name__)


@api.route('/auth/register/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    session_key = data.get('session_key')
    email = data.get('email')
    phone_number = data.get('phone_number')
    pers_photo_data = data.get('pers_photo_data')

    if User.find_by_email(email):
        return jsonify({"msg": "User already exists"}), 400

    user_id = User.create_user(username, password, first_name, last_name, session_key, email, phone_number,
                               pers_photo_data)
    return jsonify({"msg": "User registered successfully", "user_id": user_id}), 201


@api.route('/auth/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.find_by_email(email)

    if user and user['password'] == password:
        access_token = create_access_token(identity=user['id'])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401


@api.route('/posts/', methods=['GET', 'POST'])
@jwt_required()
def handle_posts():
    if request.method == 'GET':
        posts = Post.get_all_posts()
        return jsonify(posts), 200

    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')
        image_data = data.get('image_data')
        user_id = get_jwt_identity()

        post_id = Post.create_post(user_id, title, content, tags, image_data)
        return jsonify({"msg": "Post created successfully", "post_id": post_id}), 201


@api.route('/posts/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_post(id):
    post = Post.get_post_by_id(id)

    if request.method == 'GET':
        return jsonify(post), 200

    if request.method == 'PUT':
        data = request.get_json()
        title = data.get('title', post['title'])
        content = data.get('content', post['content'])
        tags = data.get('tags', post['tags'])
        image_data = data.get('image_data', post['imageData'])
        Post.update_post(id, title, content, tags, image_data)
        return jsonify({"msg": "Post updated successfully"}), 200

    if request.method == 'DELETE':
        Post.delete_post(id)
        return jsonify({"msg": "Post deleted successfully"}), 204


@api.route('/posts/<int:post_id>/comments/', methods=['GET', 'POST'])
@jwt_required()
def handle_comments(post_id):
    if request.method == 'GET':
        comments = Comment.get_comments_by_post(post_id)
        return jsonify(comments), 200

    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        image_data = data.get('image_data')
        tags = data.get('tags')
        user_id = get_jwt_identity()

        comment_id = Comment.create_comment(user_id, post_id, content, image_data, tags)
        return jsonify({"msg": "Comment created successfully", "comment_id": comment_id}), 201


@api.route('/comments/<int:id>/', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_comment(id):
    if request.method == 'PUT':
        data = request.get_json()
        content = data.get('content')
        image_data = data.get('image_data')
        tags = data.get('tags')
        Comment.update_comment(id, content, image_data, tags)
        return jsonify({"msg": "Comment updated successfully"}), 200

    if request.method == 'DELETE':
        Comment.delete_comment(id)
        return jsonify({"msg": "Comment deleted successfully"}), 204
