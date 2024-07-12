import os

class BannedWordsChecker:
    banned_words = set()

    @classmethod
    def load_banned_words(cls, file_path='banwords.txt'):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")
        with open(file_path, 'r', encoding='utf-8') as file:
            cls.banned_words = {line.strip().lower() for line in file}

    @staticmethod
    def is_contains_bad_words(text):
        words = text.lower().split()
        return any(word in BannedWordsChecker.banned_words for word in words)

# Загрузка запрещенных слов из файла (это делается один раз)
#BannedWordsChecker.load_banned_words('banwords.txt')
# Использование метода для проверки текста
# print(BannedWordsChecker.is_contains_bad_words('This is a test text'))
#Данный код возвращает True, если есть banwords и False если нет
