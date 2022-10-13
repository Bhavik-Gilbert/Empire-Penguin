from contextlib import redirect_stderr
from django.shortcuts import render, redirect

from .models import User
from .forms import LogInForm, SignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = SignUpForm()
       
    return render(request, 'signup.html', {'form': form})

def login(request):
    form = LogInForm()
    return render(request, 'login.html', {'form': form})

def feed(request):
    return render(request, 'feed.html')