from flask import jsonify, make_response


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
        self.headers["Message"] = self.message
        self.data["message"] = self.message
        self.data["status"] = self.status
        # выполнение запроса
        response = make_response(jsonify(response_body), self.status)
        for key, value in self.headers.items():
            response.headers[key] = value
        return response

    def _get_default_message(self, status):  # список кодов ошибок (в том числе кастомных)
        status_messages = {
            # статусы клиета - успешно
            200: "Successfully",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            # статусы клиента
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Token is missing",  # custom
            406: "Token is invalid",  # custom
            409: "Already exist",
            411: "Captcha required",  # custom
            412: "Undefined action",  # custom
            413: "Invalid captcha token",  # custom
            414: "Invalid captcha solution",  # custom
            415: "Incorrect action",  # custom
            416: "Exceeded time captcha limit",  # custom
            417: "Invalid user data",  # custom
            418: "Inappropriate content",  # custom
            420: "Incorrect image",
            # статусы сервера
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Database error"  # custom
        }
        return status_messages.get(status, "Unknown Status")