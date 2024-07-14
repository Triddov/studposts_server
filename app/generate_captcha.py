from captcha.image import ImageCaptcha
import random
import string
import base64
from io import BytesIO


def generate_captcha():
    captcha_length = 7
    captcha_str = ''.join(random.choices(string.ascii_letters + string.digits, k=captcha_length))
    return captcha_str


def generate_captcha_image(captcha_text):
    image = ImageCaptcha()
    data = image.generate(captcha_text)
    image_data = BytesIO(data.getvalue())
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return base64_image


def save_captcha_image():
    captcha_text = generate_captcha()
    image = ImageCaptcha()

    image.write(captcha_text, 'captcha/captcha.jpeg')


save_captcha_image()
