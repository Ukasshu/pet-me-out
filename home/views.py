from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

from .models import User, UserData, Pet


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return HttpResponse(render(request, 'home/welcomePage.html'))
    else:
        if request.method == "GET":
            _id = request.GET.get('id')
            if _id is not None:
                try:
                    _id = int(_id)
                    user = User.objects.filter(id=_id).first()
                    user_data = UserData.objects.filter(userId=user).first()
                    pets = Pet.objects.filter(ownerId=user)
                    if user is not None and user_data is not None:
                        return render(request, 'home/welcomePageLoggedIn.html',
                                      {'user': user, 'user_data': user_data, 'pets': pets,
                                       'logout': False})
                    else:
                        return redirect("/welcomePageLoggedIn")
                except ValueError:
                    return redirect("/welcomePageLoggedIn")
            else:
                if request.user.is_authenticated:
                    user = request.user
                    user_data = UserData.objects.filter(userId=user).first()
                    pets = Pet.objects.filter(ownerId=user)
                    if user is not None and user_data is not None:
                        return render(request, 'home/welcomePageLoggedIn.html',
                                      {'user': user, 'user_data': user_data, 'pets': pets, 'logout': True})
                    else:
                        return redirect("/")
                else:
                    return redirect("/")
        else:
            return redirect('/')
        return HttpResponse(render(request,'home/welcomePageLoggedIn.html'))


def register(request):
    if not request.user.is_authenticated:
        form = RegisterForm()
        return render(request, 'home/register.html', {'form': form})
    else:
        return redirect("/")


def registration(request):
    if request.method == "POST" and not request.user.is_authenticated:
        form = RegisterForm(request.POST)
        storage = messages.get_messages(request)
        storage.used = True
        if form.is_valid():
            first_name = form.cleaned_data.get('firstName')
            last_name = form.cleaned_data.get('lastName')
            mail = form.cleaned_data.get('mail')
            city = form.cleaned_data.get('city')
            contact = form.cleaned_data.get('contact')
            date_of_birth = form.cleaned_data.get('dateOfBirth')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if User.objects.filter(email=mail).count() > 0:
                messages.info(request, "This mail already has an account")
                response = HttpResponse(render(request, 'home/register.html', {'form': form}))
                return response
            else:
                user = User.objects.create_user(username, mail, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                userData = UserData.objects.create(
                    city=city,
                    contact=contact,
                    dateOfBirth=date_of_birth,
                    userId=user
                )
                messages.info(request, "Registration success")
                return redirect('/login')
        else:
            return render(request, 'home/register.html', {'form': form})
    else:
        return redirect("/")


def log_in(request):
    if not request.user.is_authenticated:
        logInForm = LogInForm()
        return render(request, 'home/login.html', {'form': logInForm})
    else:
        return redirect("/")


def login(request):
    if request.method == "POST" and not request.user.is_authenticated:
        form = LogInForm(request.POST)
        if form.is_valid():
            _username = form.cleaned_data.get('username')
            _password = form.cleaned_data.get('password')
            user = authenticate(request, username=_username, password=_password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, "Login success")
                return redirect("/")
            else:
                messages.warning(request, "Cannot authenticate user")
                return render(request, "home/login.html", {'form': form})
        else:
            messages.warning(request, "Form is not valid")
            return render(request, "home/login.html", {'form': form})
    else:
        return redirect("/")


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("/")


def profile(request):
    if request.method == "GET" and request.user.is_authenticated:
        _id = request.GET.get('id')
        if _id is not None:
            try:
                _id = int(_id)
                user = User.objects.filter(id=_id).first()
                user_data = UserData.objects.filter(userId=user).first()
                pets = Pet.objects.filter(ownerId=user)
                if user is not None and user_data is not None:
                    return render(request, 'home/profile.html',
                                  {'user': user, 'user_data': user_data, 'pets': pets,
                                   'logout': False})
                else:
                    return redirect("/profile")
            except ValueError:
                return redirect("/profile")
        else:
            if request.user.is_authenticated:
                user = request.user
                user_data = UserData.objects.filter(userId=user).first()
                pets = Pet.objects.filter(ownerId=user)
                if user is not None and user_data is not None:
                    return render(request, 'home/profile.html',
                                  {'user': user, 'user_data': user_data, 'pets': pets, 'logout': True})
                else:
                    return redirect("/")
            else:
                return redirect("/")
    else:
        return redirect('/')


def add_photo(request):
    if request.user.is_authenticated:
        form = ImageUploadForm()
        return render(request, 'home/upload_photo.html', {'form': form})
    else:
        redirect('/')


def upload_photo(request):
    if request.user.is_authenticated and request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user
            user_data = UserData.objects.filter(userId=user_id).first()
            user_data.photo = form.cleaned_data.get('image')
            user_data.save()

            return redirect('/profile')
        else:
            return redirect("/addPhoto", {'form': form})
    else:
        return redirect('/')


def add_pet(request):
    form = AddPetForm()
    return render(request, 'home/add_pet.html', {'form': form})


def create_pet(request):
    if request.user.is_authenticated and request.method == "POST":
        form = AddPetForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            _type = form.cleaned_data.get('type')
            weight = None
            if form.cleaned_data.get('weight') is not None:
                weight = float(form.cleaned_data.get('weight'))
            height = None
            if form.cleaned_data.get('height') is not None:
                height = float(form.cleaned_data.get('height'))
            other = None
            if _type == "OTHER" and form.cleaned_data.get('other') is not None:
                other = form.cleaned_data.get('other')
            breed = None
            if form.cleaned_data.get('breed') is not None:
                breed = form.cleaned_data.get('breed')
            age = form.cleaned_data.get('age')

            user = request.user

            pet = Pet.objects.create(
                name=name,
                weight=weight,
                type=_type,
                height=height,
                other=other,
                breed=breed,
                age=age,
                ownerId=user
            )

            if form.cleaned_data.get('img') is not None:
                pet.photo = form.cleaned_data.get('img')
                pet.save()

            for f in form:
                print(str(f.name) + ":" + str(f.data))
            return redirect("profile")
    return redirect("/")


def not_found(request):
    return render(request, 'home/not_found.html')


def test(request):
    return render(request, 'home/test.html')
