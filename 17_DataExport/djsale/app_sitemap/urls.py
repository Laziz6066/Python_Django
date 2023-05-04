from django.urls import path
from .views import *


urlpatterns = [
    path('main_page', main_page, name='main_page'),
    path('about_us', about_us, name='about_us'),
    path('contacts', contacts, name='contacts'),
    path('list_of_housing_for-sale.html', House.as_view(), name='list_of_housing_for-sale'),
    path('news', News.as_view(), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='house-item'),
]