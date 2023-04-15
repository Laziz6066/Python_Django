from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('blog/<int:pk>/detail/', DetailViewNews.as_view(), name='detail'),
    path('login', AppLogin.as_view(), name='login'),
    path('logout', LogoutNewsView.as_view(), name='logout'),
    path('another_register', another_register_view, name='another_register'),
    path('acc', Accounts.as_view(), name='acc'),
    path('create_news', NewsCreationView.as_view(), name='create_news'),
    # path('blog/<int:pk>/news_edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('moderator', ModeratorViews.as_view(), name='moderator'),
    path('blog/<int:pk>/mod_detail/', ModDetail.as_view(), name='mod_detail'),
    path('users', ModUserViews.as_view(), name='users'),
    path('blog/<int:pk>/users_detail/', UserDetailView.as_view(success_url='/blog'), name='users_detail'),
]
