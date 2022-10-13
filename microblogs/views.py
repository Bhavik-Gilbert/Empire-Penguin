from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User
from .forms import LogInForm, SignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
       
    return render(request, 'signup.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('feed')

        # Add error messages
        messages.add_message(request, messages.ERROR, "The username or passsword is incorrect") 

    form = LogInForm()
    return render(request, 'login.html', {'form': form})

def feed(request):
    return render(request, 'feed.html')