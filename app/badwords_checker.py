import os


class BannedWordsChecker:  # класс валидации данных на плохие слова
    banned_words = set()

    @classmethod
    def load_banned_words(cls, file_path='badwords.txt'):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")
        with open(file_path, 'r', encoding='utf-8') as file:
            cls.banned_words = {line.strip().lower() for line in file}

    @staticmethod
    def bad_words(text):
        words = text.lower().split()
        if any(word in BannedWordsChecker.banned_words for word in words):
            return False  # если найдено хоть одно badword, вернуть пустую строку
        else:
            return text  # если badwords не найдено, вернуть этот же текст
