from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64
import os


load_dotenv()

UPLOAD_FOLDER_ICONS = os.getenv('UPLOAD_FOLDER_ICONS')
UPLOAD_FOLDER_IMAGES = os.getenv('UPLOAD_FOLDER_IMAGES')


def check_user_data(data):  # метод проверки данных при регистрации
    # обязательные поля
    required_fields = ['login', 'password', 'first_name', 'sur_name']

    # поля, которые не нужно проверять
    ignore_fields = ['input_captcha', 'captcha_token', 'pers_photo_data']

    # поля, для которых есть значения минимальной длины
    min_length_fields = ['first_name', 'sur_name', 'middle_name']
    min_length = 2

    # проверка обязательных полей
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

        if not data[field] or ' ' in data[field]:
            return False, f"{field} should not be empty or contain spaces"

    max_lengths = {  # список ограничений полей в базе
        'login': 255,
        'password': 128,
        'first_name': 50,
        'sur_name': 50,
        'middle_name': 50,
        'email': 36,
        'phone_number': 20,
        'pers_photo_data': 255
    }

    # проверка длины полей
    for field, max_length in max_lengths.items():
        if (field in data) and (field not in ignore_fields) and (len(data[field]) > max_length):
            return False, f"{field} exceeds maximum length of {max_length} characters"

    # проверка минимальной длины полей
    if 'middle_name' not in data or not data['middle_name']:
        min_length_fields.remove('middle_name')

    for field in min_length_fields:
        if (field in data) and (field not in ignore_fields) and (len(data[field]) < min_length):
            return False, f"{field} should be at least 2 characters long"

    # проверка email на валидность
    if ('email' in data) and ('email' not in ignore_fields) and ('@' not in data['email']):
        return False, "Invalid email format"

    return True, None  # возвращаем валидны ли данные и описание ошибки


def check_post_data(data):  # метод проверки данных поста  НЕ ТЕСТИЛОСЬ ЕЩЕ!!!
    required_fields = ['user_login', 'title', 'content']

    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
        if data[field] == '' or data[field].isspace() == True:
            return False, f'{field} should not be empty or consist of spaces'

    # проверка на длину полей
    max_lengths = {
        'title': 200,
        'tags': 200,
        'image_data': 255,
    }

    for field, max_len in max_lengths.items():
        if field in data and len(data[field]) > max_len:
            return False, f'{field} exceeds maximum length of {max_len} characters'

    return True, None


def check_comment_data(data):  # метод проверки данных коммента  НЕ ТЕСТИЛОСЬ ЕЩЕ!!!
    # проверка на пустоту полей
    required_fields = ['user_login', 'post_id', 'content']

    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
        if data[field] == '' or data[field].isspace() == True:
            return False, f'{field} should not be empty or consist of spaces'

    # проверка на длину полей
    max_lengths = {
        'tags': 200,
    }

    for field, max_len in max_lengths.items():
        if field in data and len(data[field]) > max_len:
            return False, f'{field} exceeds maximum length of {max_len} characters'

    return True, None


def is_image_valid(image_base64):  # функция валидации изображения
    try:
        # декодируем изображение из base64
        image_data = base64.b64decode(image_base64)

        # Проверка размера файла
        size_in_mb = len(image_data) / (1024 * 1024)  # размер в мегабайтах
        if size_in_mb > 2:
            return False

        # Проверка валидности файла
        image = Image.open(BytesIO(image_data))
        image.verify()  # Фактическая проверка

        return True

    except Exception:
        return False


def is_icon_square(base64_image):  # проверка иконки на равные стороны
    # декодируем изображение из base64
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))

    width, height = image.size

    return width == height


def save_icon(image_base64, file_name):  # сохранение иконки пользователя
    icon_path = os.path.join(UPLOAD_FOLDER_ICONS, file_name)
    image = Image.open(BytesIO(base64.b64decode(image_base64)))

    image.save(icon_path)

    return icon_path


def save_image(image_base64, file_name):  # сохранение изображения
    image_path = os.path.join(UPLOAD_FOLDER_IMAGES, file_name)
    image = Image.open(BytesIO(base64.b64decode(image_base64)))

    image.save(image_path)

    return image_path
