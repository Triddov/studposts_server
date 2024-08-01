from flask import jsonify, make_response
from datetime import datetime


def log_status(error, module_name):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('date:%m/%d/%y time:%H:%M:%S')}"
                       f" | error message: {error} | in module: {module_name}\n")


class Response:  # класс ответов, ошибок и сообщений в теле запросов
    def __init__(self, data=None, status=200, message="OK"):
        self.data = data if data is not None else {}
        self.status = status
        self.message = message or self._get_default_message(status)
        self.headers = {}

    def set_status(self, status):
        self.status = status
        self.message = self._get_default_message(status)

    def set_data(self, data):
        self.data = data

    def set_header(self, key, value):
        self.headers[key] = value

    def set_message(self, message):
        self.message = message

    def send(self):
        # данные и сообщение
        response_body = self.data
        self.data["message"] = self.message
        self.data["status"] = self.status
        # выполнение запроса
        response = make_response(jsonify(response_body), 200) #self.status
        for key, value in self.headers.items():
            response.headers[key] = value
        return response

    def _get_default_message(self, status):  # список кодов ошибок (в том числе кастомных)
        status_messages = {
            # статусы клиета - успешно
            200: "Successfully",
            201: "Created",
            202: "Accepted",
            205: "Successfully update",  # custom
            206: "Successfully delete",  # custom
            # статусы клиента
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Token is missing",  # custom
            406: "Token is invalid",  # custom
            409: "Already exist",
            410: "Invalid login or password in token",  # custom
            411: "Captcha required",  # custom
            412: "Undefined action",  # custom
            413: "Invalid captcha token",  # custom
            414: "Invalid captcha solution",  # custom
            415: "Incorrect action",  # custom
            416: "Exceeded time captcha limit",  # custom
            417: "Invalid data",  # custom
            418: "Inappropriate content",  # custom
            419: "Data not found",
            420: "Incorrect image",  # custom
            421: "Insufficient rights",
            # статусы сервера
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Database error"  # custom
        }
        return status_messages.get(status, "Unknown Status")
