from django.shortcuts import render
from django.views.generic import TemplateView

count_request = 0

class Advertisement(TemplateView):
    template_name = 'advertisements/advertisement_list.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['advertisements'] = [
            'Мастер на час',
            'Выведение из запоя',
            'Услуги экскаватора-погрузчика, гидромолота, ямобура'
        ]

        contex['count_request'] = count_request
        return contex


    def post(self, request, *args, **kwargs):
        global count_request
        count_request += 1

        contex = self.get_context_data(**kwargs)
        contex['post_response'] = 'Статья успешно создана'
        return self.render_to_response(contex)


class Contacts(TemplateView):
    template_name = 'advertisements/contact.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['company'] = {
            'address': 'Улица Шибаева дом 34',
            "email": 'Shibaeva@gmail.com',
            'number': '+79546321548'
        }
        return contex


class About(TemplateView):
    template_name = 'advertisements/about.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['company'] = {
            'name': "SSS electronics",
            'description': 'У нас самый большой ассортимент бытовой техники по самым низким ценам'
        }
        return contex


class Home(TemplateView):
    template_name = template_name = 'advertisements/home_page.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['regions'] = ['Москва', 'Питер', 'Владивосток']
        contex['categories'] = ['Хобби', 'Транспорт', 'Электроника', 'отдых']
        return contex