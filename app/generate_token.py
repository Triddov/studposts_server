import uuid


def generate_unique_token():  # генерация токена юзера
    return str(uuid.uuid4())


def encrypt_decrypt(text, key):  # шифрование и дешифрование текста капчи

    text_bytes = bytearray(text, 'utf-8')  # Преобразуем строку в байтовый массив, чтобы работать с кодами символов (ASCII)
    key_bytes = bytearray(key, 'utf-8')

    encrypted_bytes = bytearray()  # Создаем пустой байтовый массив для хранения зашифрованного текста

    # Циклически применяем XOR к каждому байту текста с соответствующим байтом ключа
    for i in range(len(text_bytes)):
        encrypted_byte = text_bytes[i] ^ key_bytes[i % len(key_bytes)]
        encrypted_bytes.append(encrypted_byte)

    # Преобразуем зашифрованный байтовый массив обратно в строку и возвращаем результат
    encrypted_text = encrypted_bytes.decode('utf-8')
    return encrypted_text

