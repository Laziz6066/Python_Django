from django.urls import path
from . import views

urlpatterns = [
    path('advertisements', views.Advertisement.as_view(), name='advertisement_list'),
    path("contact", views.Contacts.as_view(), name='contact'),
    path("about/", views.About.as_view(), name='about'),
    path("", views.Home.as_view(), name='home')
]
