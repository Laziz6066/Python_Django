from django.http import HttpResponse
import random
from django.views import View

task = [
    'Установить python', 'Установить django', 'Запустить сервер', 'Порадоваться результату',
        'Отправить отчет преподавателю', 'Изучить SQL', 'Изучить Django', 'Изучить python advanced',
        'Отправить задание', 'Переделать задание'
]
class ToDoView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<ul>'
                            f'<li>{random.choice(task)}</li>'
                            f'<li>{random.choice(task)}</li>'
                            f'<li>{random.choice(task)}</li>'
                            f'<li>{random.choice(task)}</li>'
                            f'<li>{random.choice(task)}<li>'
                            '</ul>')
