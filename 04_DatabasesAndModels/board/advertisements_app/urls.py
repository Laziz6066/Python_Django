from django.urls import path
from .views import *

urlpatterns = [
    path('advertisement', Home.as_view(), name='home'),
    path('advertisement/<int:pk>', Detail.as_view(), name='detail'),
]
