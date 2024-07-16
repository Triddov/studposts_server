from captcha.image import ImageCaptcha
import random, string, base64
from io import BytesIO


def generate_captcha():  # метод генерации текста капчи
    captcha_length = 6
    captcha_str = ''.join(random.choices(string.ascii_letters + string.digits, k=captcha_length))
    return captcha_str  # текст капчи, который будет на изображении


def generate_captcha_image(captcha_text):  # метод генерации изображения капчи и перевод его в строку base64
    image = ImageCaptcha()
    data = image.generate(captcha_text)
    image_data = BytesIO(data.getvalue())
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return base64_image  # изображение капчи, закодированное как base64
