from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64
import os
import re


load_dotenv()

UPLOAD_FOLDER_ICONS = os.getenv('UPLOAD_FOLDER_ICONS')
UPLOAD_FOLDER_IMAGES = os.getenv('UPLOAD_FOLDER_IMAGES')

max_lengths = {  # список ограничений полей в базе
    # поля юзера:
    'login': 255,
    'password': 128,
    'first_name': 50,
    'sur_name': 50,
    'middle_name': 50,
    'email': 36,
    'phone_number': 12,
    'pers_photo_data': 255,
    # поля постов:
    'title': 200,
    'tags': 200,
    'image_data': 255,
}


def check_bad_words(*fields_to_check):
    file_path = 'badwords.txt'

    # если нет файла с badwords
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")

    # открываем и считываем файл
    with open(file_path, 'r', encoding='utf-8') as file:
        bad_words = {line.strip().lower() for line in file}

    # устанавливаем поля валидации
    required_fields = list(fields_to_check)

    # регулярное выражение для удаления знаков препинания
    pattern = re.compile(r'[^\w\s]', re.UNICODE)

    # пропускаем поле, если его значение None
    for field in required_fields:
        if field is None:
            continue

        # удаление знаков препинания и подобного
        cleaned_field = pattern.sub('', field)
        words = cleaned_field.lower().split()

        # если найдено хотя бы одно слово - проверка не пройдена
        if any(word in bad_words for word in words):
            return False

    return True


def load_nginx_blacklist(filepath):
    banned_ips = set()
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip().startswith('deny'):
                parts = line.split()
                if len(parts) > 1:
                    ip = parts[1].rstrip(';')
                    banned_ips.add(ip)
    return banned_ips


def check_user_data(data, action = 'register'):
    
    # поля, которые пользователь может менять и устанавливать в принципе
    allowed_fields = ['login', 'password', 'first_name', 'sur_name', 'middle_name', 'email', 'phone_number']
    
    # обязательные поля для регистрации
    if action == 'register':
        required_fields = ['login', 'password', 'first_name', 'sur_name']

        # проверка обязательных полей
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

            if not data[field]:
                return False, f"{field} should not be empty"
    
    # проверка всех полей на содержание пробельных символов
    for field in allowed_fields:
        if field in data and ' ' in data[field]:
            return False, f"{field} should not contain spaces"


    # поля, для которых есть значения минимальной длины
    min_length_fields = ['first_name', 'sur_name', 'middle_name']
    min_length = 2

    # проверка минимальной длины полей
    for field in min_length_fields:
        if (field in data) and (data[field]):  # только если поле существует и не пустое
            if len(data[field]) < min_length:
                return False, f"{field} should be at least 2 characters long"

    # проверка на превышение максимальной длины полей
    for field, max_length in max_lengths.items():
        if (field in data) and (field in allowed_fields) and (len(data[field]) > max_length):
            return False, f"{field} exceeds maximum length of {max_length} characters"


    # проверка email на валидность
    if ('email' in data) and (data['email']) and ('@' not in data['email']):
        return False, "Invalid email format"

    # проверка российского номера телефона
    phone_pattern = re.compile(r'^(?:\+7|8)?\d{10}$')
    if 'phone_number' in data and data['phone_number']:
        if not phone_pattern.match(data['phone_number']):
            return False, "Invalid phone number format"

    # проверка на отсутствие русских букв в логине и пароле
    non_russian_pattern = re.compile(r'^[^\u0400-\u04FF]*$')
    for field in ['login', 'password']:
        if field in data and data[field]:
            if not non_russian_pattern.match(data[field]):
                return False, f"{field} should not contain Russian letters"
    
    
    return True, None  # возвращаем валидны ли данные и описание ошибки


def check_post_data(data):  # метод проверки данных поста
    # обязательные поля
    required_fields = ['title', 'content']

    # поля, которые не нужно проверять
    ignore_fields = ['image_data']

    # проверка обязательных полей
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
        if data[field].isspace():
            return False, f'{field} should not be empty'

    # проверка длины полей
    for field, max_len in max_lengths.items():
        if (field in data) and (field not in ignore_fields) and (len(data[field]) > max_len):
            return False, f'{field} exceeds maximum length of {max_len} characters'

    return True, None


def check_comment_data(data):  # метод проверки данных коммента
    required_fields = ['content']

    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
        if data[field].isspace():
            return False, f'{field} should not be empty'

    # проверка длины полей
    for field, max_len in max_lengths.items():
        if field in data and len(data[field]) > max_len:
            return False, f'{field} exceeds maximum length of {max_len} characters'

    return True, None


def is_image_valid(image_base64: str) -> bool:  # функция валидации изображения
    try:
        # декодируем изображение из base64
        image_data = base64.b64decode(image_base64)

        # Проверка валидности файла
        image = Image.open(BytesIO(image_data))
        image.verify()  # Фактическая проверка

        return True

    except:
        return False


def is_icon_square(base64_image: str) -> bool:  # проверка иконки на равные стороны
    # декодируем изображение из base64
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))

    width, height = image.size

    return width == height


def check_image_aspect_ratio(image_base64: str) -> bool:  # проверка соотношения сторон изображения
    # декодируем изображение из base6
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))

    width, height = image.size

    ratio = 4  # максильно допустимое соотношение
    # Проверка соотношения ширины и высоты
    if width / height > ratio or height / width > ratio:
        return False

    return True


def save_icon(image_base64, file_name):
    icon_path = os.path.join(UPLOAD_FOLDER_ICONS, file_name)

    # Проверка существования директории и создание, если она отсутствует
    if not os.path.exists(UPLOAD_FOLDER_ICONS):
        os.makedirs(UPLOAD_FOLDER_ICONS)

    image = Image.open(BytesIO(base64.b64decode(image_base64)))
    image.save(icon_path)

    return icon_path


def save_image(image_base64, file_name):
    # Создаем путь файла
    image_path = os.path.join(UPLOAD_FOLDER_IMAGES, file_name)
    image = Image.open(BytesIO(base64.b64decode(image_base64)))

    # Сохраняем изображение по указанному пути
    image.save(image_path)

    # Возвращаем путь к изображению с правильными слэшами для текущей ОС
    return image_path.replace('\\', '/')
