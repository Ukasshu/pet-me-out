from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import RegisterForm, LogInForm
from django.contrib import messages
from django.shortcuts import render

from .models import User
from .models import UserData


# Create your views here.
def home(request):
    # template = loader.get_template('home/welcomePage.html')
    return HttpResponse(render(request, 'home/welcomePage.html'))


def register(request):
    form = RegisterForm()
    return render(request, 'home/register.html', {'form': form})


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
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
                # response.write("This mail already has an account")
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
        return redirect("/home")


def log_in(request):
    logInForm = LogInForm()
    if 'id' in request.session:
        print(request.session['id'])
        print(request.session.get_expire_at_browser_close())
    return render(request, 'home/login.html', {'form': logInForm})


def login(request):
    if request.method == "POST":
        _username = request.POST['username']
        _password = request.POST['password']
        user = User.objects.filter(mail=_username).first()
        if user is None:
            messages.info(request, 'Before login you have to register')
            return redirect("/login")
        else:
            if user.password == _password:
                request.session['id'] = user.id  # TODO: testowanie sesji
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                    return render(request, 'home/profile.html', {'user': user})
            elif not user.password == _password:
                messages.info(request, 'Your password is not valid, please check it out!')
                return redirect("/login")
            else:
                messages.info(request,
                              'Your login is not valid.' + "\n" + 'If you are not registered, please see the option below the login form.')
                return redirect("/login")
    else:
        return redirect("/")


def profile(request):
    if request.method == "GET":
        if 'id' not in request.GET:
            _id = request.session['id']
            user = User.objects.filter(id=_id).first()
            if not user is None:
                return render(request, 'home/profile.html', {'user': user})
            else:
                return redirect("/")
        else:
            _id = request.GET['id']
            user = User.objects.filter(id=_id).first()
            if not user is None:
                return render(request, 'home/profile.html', {'user': user})
            else:
                return redirect("/")
    else:
        return redirect("/")
