from django.urls import path
from app_rss.feeds import LatestHouseFedd


urlpatterns = [
    path('latest/feed', LatestHouseFedd())
]