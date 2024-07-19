import os
import unittest
from flask import Flask
from flask_jwt_extended import JWTManager
from routes import api, get_image

class TestImageEndpoints(unittest.TestCase):
    def setUp(self):
        # Создаем тестовое приложение Flask
        self.app = Flask(__name__)
        self.app.register_blueprint(api)  # Регистрируем наш Blueprint
        self.app.config['JWT_SECRET_KEY'] = 'jwt_triddov228'  # Устанавливаем секретный ключ для JWT
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        jwt = JWTManager(self.app)

        # Создаем необходимые директории для тестов
        if not os.path.exists('source/userPostImages'):
            os.makedirs('source/userPostImages')
        if not os.path.exists('source/userProfileIcons'):
            os.makedirs('source/userProfileIcons')

        # Создаем тестовые изображения
        with open('source/userPostImages/post_test.png', 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\x0c\x16)\x00\x00\x00\x00IEND\xaeB`\x82')
        with open('source/userProfileIcons/profile_test.png', 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\x0c\x16)\x00\x00\x00\x00IEND\xaeB`\x82')

    def tearDown(self):
        # Удаляем тестовые изображения и директории после тестов
        if os.path.exists('source/userPostImages/post_test.png'):
            os.remove('source/userPostImages/post_test.png')
        if os.path.exists('source/userProfileIcons/profile_test.png'):
            os.remove('source/userProfileIcons/profile_test.png')
        if os.path.exists('source/userPostImages'):
            os.rmdir('source/userPostImages')
        if os.path.exists('source/userProfileIcons'):
            os.rmdir('source/userProfileIcons')

    def test_get_post_image(self):
        # Тестируем получение изображения поста
        response = self.client.get('/images/post_test.png')
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус-код 200
        self.assertEqual(response.content_type, 'image/png')  # Проверяем, что возвращаемый контент - это изображение PNG


if __name__ == '__main__':
    unittest.main()
