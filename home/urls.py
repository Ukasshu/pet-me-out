from django.urls import path, re_path
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
    path('uploadPhoto', views.upload_photo, name='uploadPhoto'),
    path('addPet', views.add_pet, name='add_pet'),
    path('createPet', views.create_pet, name='create_pet'),
    path("404", views.not_found, name='not_found'),
    path("addGuestAdvert", views.add_guest_advert, name='add_guest_advert'),
    path("createGuestAdvert", views.create_guest_advert, name='create_guest_advert'),
    path("addHostAdvert", views.add_host_advert, name='add_host_advert'),
    path("createHostAdvert", views.create_host_advert, name='create_host_advert'),
    path("removePet", views.remove_pet, name="remove_pet"),
    path("deletePet", views.delete_pet, name="delete_pet"),
    path("stayRequest", views.stay_req, name="stay_req"),
    path("stayPossibility", views.stay_pos, name="stay_pos"),
    path("proposeStay", views.propose_stay, name="propose_stay")
]
