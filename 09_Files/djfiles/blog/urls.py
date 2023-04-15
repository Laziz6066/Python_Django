from django.urls import path
from .views import *


urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('blog_entry', BlogEntryView.as_view(), name='blog_entry'),
    path('<int:pk>/detail', BlogDetail.as_view(), name='detail'),
    path('login', AppLogin.as_view(), name='login'),
    path('logout', LogoutNewsView.as_view(), name='logout'),
    path('another_register', AnotherRegisterView.as_view(), name='another_register'),
    path('acc', Accounts.as_view(), name='acc'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('upload/<int:pk>/', UploadFilesView.as_view(), name='upload_files'),
    path('upload_csv', UpdateCsvView.as_view(), name='upload_csv'),

]
