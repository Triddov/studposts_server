from captcha.image import ImageCaptcha
import random
import string
import base64
from io import BytesIO


# Функция для генерации текста капчи
def generate_captcha(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Функция для создания и сохранения изображения капчи в base64
def generate_captcha_image(captcha_text):
    image = ImageCaptcha(width=240, height=90)
    data = image.generate(captcha_text)
    image_data = BytesIO(data.getvalue())
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return base64_image  # изображение капчи, закодированное в формат base64
