from PIL import Image


def check_user_data(data):
    # список обязательных полей
    required_fields = ['login', 'password', 'first_name', 'sur_name']

    # поля, которые не нужно проверять
    ignore_fields = ['input_captcha', 'captcha_token']

    # проверка обязательных полей
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not data[field] or ' ' in data[field]:
            print(123)
            return False, f"{field} should not be empty or contain spaces"

    max_lengths = {
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
        if (field in data) and (field not in ignore_fields) and (len(data[field].encode('utf-8')) > max_length):
            return False, f"{field} exceeds maximum length of {max_length} bytes"

    # проверка минимальной длины полей имени
    for field in ['first_name', 'sur_name']:
        if (field in data) and (field not in ignore_fields) and (len(data[field]) < 2):
            return False, f"{field} should be at least 2 characters long"

    # проверка email на валидность
    if ('email' in data) and ('email' not in ignore_fields) and ('@' not in data['email']):
        return False, "Invalid email format"

    return True, None  # возвращаем валидны ли данные и мессадж ошибки



def check_post_data():
    pass


def check_comment_data():
    pass




def valid_image():
    pass


def is_image_square(image_path):  # проверка "квадратности" изображения
    with Image.open(image_path) as img:
        width, height = img.size
        return width == height
