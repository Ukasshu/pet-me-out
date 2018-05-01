from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .forms import RegisterForm

# Create your views here.
def home(request):
   # template = loader.get_template('home/welcomePage.html')
    return HttpResponse(render(request, 'home/welcomePage.html'))

def register(request):
    form = RegisterForm()
    return render(request, 'home/registration.html', {'form': form})
