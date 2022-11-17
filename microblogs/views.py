from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import User, Post
from .forms import LogInForm, SignUpForm, PostForm
from .helpers import login_prohibited

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
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

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                redirect_url = request.POST.get('next') or 'feed'
                return redirect(redirect_url)

        # Add error messages
        messages.add_message(request, messages.ERROR, "The username or password is incorrect") 

    form = LogInForm()

    # dealing with getting next redirect for required login page
    next = request.GET.get('next') or ''

    return render(request, 'login.html', {'form': form, 'next':next})

def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def feed(request):
    form = PostForm()
    return render(request, 'feed.html', {'form': form})

@login_required
def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user
            form = PostForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                post = Post.objects.create(author=current_user, text=text)
                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
