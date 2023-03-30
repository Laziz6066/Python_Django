from django.urls import path
from .views import *

urlpatterns = [
    path('', advertisement_list, name='home'),
    path('list', list, name='list'),
    path('classes', classes, name='classes'),
    path('dictionaries', dictionaries, name='dictionaries'),
    path('functions', functions, name='functions'),
    path('tuples', tuples, name='tuples'),
]

