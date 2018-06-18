from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

import datetime

from .models import User, UserData, Pet, StayPossibility, StayRequest


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
        return HttpResponse(render(request, 'home/welcomePageLoggedIn.html'))


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
                stay_requests = StayRequest.objects.filter(userId=user)
                stay_possibilities = StayPossibility.objects.filter(userId=user)

                if user is not None and user_data is not None:
                    return render(request, 'home/profile.html',
                                  {'user': user, 'user_data': user_data, 'pets': pets, 'stay_requests': stay_requests,
                                   'stay_possibilities': stay_possibilities,
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
                stay_requests = StayRequest.objects.filter(userId=user)
                stay_possibilities = StayPossibility.objects.filter(userId=user)
                if user is not None and user_data is not None:
                    return render(request, 'home/profile.html',
                                  {'user': user, 'user_data': user_data, 'pets': pets, 'stay_requests': stay_requests,
                                   'stay_possibilities': stay_possibilities, 'logout': True})
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
    if request.user.is_authenticated:
        form = AddPetForm()
        return render(request, 'home/add_pet.html', {'form': form})
    else:
        return redirect("/")


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
    if request.user.is_authenticated:
        return render(request, 'home/not_found.html')
    else:
        return redirect("/")


def add_guest_advert(request):
    if request.user.is_authenticated:
        pets_choices = tuple(map(lambda p: (p.id, p.name), Pet.objects.filter(ownerId=request.user)))
        form = AddGuestAdvertForm(pets_choices, None)
        return render(request, 'home/add_guest_advert.html', {'form': form})
    else:
        return redirect("/")


def add_host_advert(request):
    if request.user.is_authenticated:
        form = AddHostAdvertForm()
        return render(request, 'home/add_host_advert.html', {'form': form})
    else:
        return redirect("/")


def create_guest_advert(request):
    if request.user.is_authenticated and request.method == "POST":
        pets_choices = tuple(map(lambda p: (p.id, p.name), Pet.objects.filter(ownerId=request.user)))
        form = AddGuestAdvertForm(pets_choices, request.POST)
        if form.is_valid():
            dateFrom = form.cleaned_data.get("dateFrom")
            dateTo = form.cleaned_data.get("dateTo")
            if dateFrom > dateTo:
                messages.warning(request, "Wrong time period ('from' after 'to')")
                return render(request, 'home/add_guest_advert.html', {'form': form})
            elif dateFrom < datetime.datetime.today().date():
                messages.warning(request, "🚀 Time travels unavailable yet 🚀")
                return render(request, 'home/add_guest_advert.html', {'form': form})
            else:
                user = request.user
                for petId in form.cleaned_data.get('pets'):
                    pet = Pet.objects.filter(id=petId).first()
                    StayRequest.objects.create(
                        startDate=dateFrom,
                        endDate=dateTo,
                        userId=user,
                        petId=pet
                    )
                messages.info(request, "Advert successfully added")
                return redirect('/profile')
        else:
            return render(request, 'home/add_guest_advert.html', {'form': form})
    else:
        return redirect("/")


def create_host_advert(request):
    if request.user.is_authenticated and request.method == "POST":
        form = AddHostAdvertForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data.get('dateFrom')
            date_to = form.cleaned_data.get('dateTo')
            if date_from > date_to:
                messages.warning(request, "Wrong time period ('from' after 'to')")
                return render(request, 'home/add_host_advert.html', {'form': form})
            elif date_from < datetime.datetime.today().date():
                messages.warning(request, "🚀 Time travels unavailable yet 🚀")
                return render(request, 'home/add_guest_advert.html', {'form': form})
            else:
                pet_type = form.cleaned_data.get('type')
                StayPossibility.objects.create(
                    startDate=date_from,
                    endDate=date_to,
                    userId=request.user,
                    petType=pet_type
                )
                messages.info(request, "Advert successfully added")
                return redirect('/profile')
        else:
            return render(request, "home/add_host_advert.html", {'form': form})
    else:
        return redirect("/")


def remove_pet(request):
    if request.user.is_authenticated and request.method == "GET" and request.GET.get('petId') is not None:
        pet_id = request.GET.get('petId')
        pet = Pet.objects.filter(id=pet_id, ownerId=request.user).first()
        if pet is None:
            return redirect('/404')
        else:
            return render(request, 'home/remove_pet.html', {'pet': pet})
    else:
        redirect('/profile')


def delete_pet(request):
    if request.user.is_authenticated and request.method == "POST" and request.POST.get('id') is not None:
        Pet.objects.filter(id=request.POST.get('id')).delete()
        messages.info(request, "Your pet has been deleted")
        return redirect("/profile")
    else:
        return redirect("/")


def stay_req(request):
    if request.user.is_authenticated and request.method == "GET" and request.GET.get('id') is not None:
        st_rq = StayRequest.objects.filter(id=request.GET.get('id')).first()
        if st_rq is None:
            return redirect("/404")
        else:
            cityArg = UserData.objects.filter(userId=st_rq.userId).first().city
            recom = None
            if st_rq.userId == request.user:
                city = UserData.objects.filter(userId=request.user).first().city
                recom = StayPossibility.objects.filter(userId__userdata__city=city)\
                    .filter(startDate__lte=st_rq.startDate)\
                    .filter(endDate__gte=st_rq.endDate)\
                    .exclude(userId=request.user)[:5]
            return render(request, "home/stay_request.html", {"recom": recom, "st_rq": st_rq, 'city': cityArg})
    else:
        return redirect("/")


def stay_pos(request):
    if request.user.is_authenticated and request.method == "GET" and request.GET.get('id') is not None:
        st_ps = StayPossibility.objects.filter(id=request.GET.get('id')).first()
        if st_ps is None:
            return redirect("/404")
        else:
            cityArg = UserData.objects.filter(userId=st_ps.userId).first().city
            recom = None
            if st_ps.userId == request.user:
                city = UserData.objects.filter(userId=request.user).first().city
                recom = StayRequest.objects.filter(userId__userdata__city=city) \
                            .filter(startDate__gte=st_ps.startDate) \
                            .filter(endDate__lte=st_ps.endDate)\
                            .exclude(userId=request.user)
                if st_ps.petType != 'All':
                    recom = recom.filter(petId__type=st_ps.petType)
                recom = recom[:5]
            return render(request, "home/stay_possibility.html", {"recom": recom, "st_ps": st_ps, 'city': cityArg})
    else:
        return redirect("/")


def propose_stay(request):
    if request.user.is_authenticated and request.method=="POST":
        return "XD"
    return "XD"