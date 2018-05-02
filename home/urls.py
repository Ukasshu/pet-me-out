from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name='register'),
    path('registration', views.registration, name='registration')
]
