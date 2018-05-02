from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader

from .forms import RegisterForm

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
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            mail = form.cleaned_data['mail']
            city = form.cleaned_data['city']
            contact = form.cleaned_data['contact']
            dateOfBirth = form.cleaned_data['dateOfBirth']
            password = form.cleaned_data['password']
            user = User.objects.create(
                firstName = firstName,
                lastName = lastName,
                mail = mail,
                city = city,
                contact = contact,
                dateOfBirth = dateOfBirth,
                password = password,
            )
            return HttpResponse("<h2>SUCCESS</h2>")
    else:
        return redirect("/home")