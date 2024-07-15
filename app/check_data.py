from PIL import Image


def check_user_data():
    pass


def check_post_data():
    pass


def check_comment_data():
    pass




def is_image_square(image_path):  # проверка "квадратности" изображения
    with Image.open(image_path) as img:
        width, height = img.size
        return width == height
