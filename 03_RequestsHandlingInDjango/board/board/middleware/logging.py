from datetime import datetime
from django.http import HttpRequest, HttpResponse

class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestap = datetime.today()

        response = self.get_response(request)

        with open('board/middleware/logging.txt', 'w', encoding='utf-8') as file:
            file.write(f'Время запроса: {str(timestap)}\n'
                       f'Запрошенный URL: {request.build_absolute_uri()}\n'
                       f'HTTP метод: {HttpResponse(request.method)}')

        return response