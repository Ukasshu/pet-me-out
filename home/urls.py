from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name='register'),
    path('registration', views.registration, name='registration'),
    path('login', views.log_in, name='login'),
    path('verify_user', views.login, name='verify_user'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('addPhoto', views.add_photo, name='addPhoto'),
    path('uploadPhoto', views.upload_photo, name='uploadPhoto')
]
