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
        response_body = self.data
        response = make_response(jsonify(response_body), self.status)
        for key, value in self.headers.items():
            response.headers[key] = value
        return response

    def _get_default_message(self, status):  # список кодов ошибок (в том числе кастомных)
        status_messages = {
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Token is missing",
            406: "Token is invalid",
            409: "Already exist",
            411: "Captcha required",
            412: "Undefined action",
            413: "Invalid captcha token",
            414: "Invalid captcha solution",
            415: "Incorrect action",
            416: "Exceeded time captcha limit",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }
        return status_messages.get(status, "Unknown Status")
