from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import RegisterForm, LogInForm
from django.contrib import messages
from django.shortcuts import render

from .models import User


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
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            mail = form.cleaned_data['mail']
            city = form.cleaned_data['city']
            contact = form.cleaned_data['contact']
            date_of_birth = form.cleaned_data['dateOfBirth']
            password = form.cleaned_data['password']
            if User.objects.filter(mail=mail).count() > 0:
                response = HttpResponse(render(request, 'home/register.html', {'form': form}))
                response.write("This mail already has an account")
                return response
            else:
                user = User.objects.create(
                    firstName=first_name,
                    lastName=last_name,
                    mail=mail,
                    city=city,
                    contact=contact,
                    dateOfBirth=date_of_birth,
                    password=password,
                )
                return HttpResponse("<h2>SUCCESS</h2>")
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
        try:
            user = User.objects.filter(mail=_username).first()
            if user.password == _password:
                request.session['id'] = user.id  # TODO: testowanie sesji
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                return HttpResponse("<h2>Success :)</h2>")
            elif not user.password == _password:
                messages.info(request, 'Your password is not valid, please check it out!')
                return redirect("/login")
            else:
                messages.info(request,
                              'Your login is not valid.' + "\n" + 'If you are not registered, please see the option below the login form.')
                return redirect("/login")
        except User.DoesNotExist:
            messages.info(request, 'Before login you have to register')
            return redirect("/login")
