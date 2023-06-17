from django.contrib.auth.views import LogoutView
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('home/', home_view, name='home'),
    path('admin-home', admin_home_view, name='admin_home'),
    path('create-center/', create_center_view, name='create_center'),
    path('logout/', logout_view, name='logout'),
    path('centers/', center_list, name='center_list'),
    path('access-denied/', access_denied_view, name='access_denied'),
    path('admin-centers/', admin_center_list, name='admin_center_list'),
    path('center/<int:center_id>/delete/', delete_center, name='delete_center'),
    path('center/<int:center_id>/book/', book_center, name='book_center'),
    path('', welcome, name='welcome')
]
