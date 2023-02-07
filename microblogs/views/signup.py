from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..forms import SignUpForm
from ..models import User
from ..helpers import login_prohibited


@login_prohibited
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: SignUpForm = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user: User = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form: SignUpForm = SignUpForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def edit_user_profile_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user

    if request.method == 'POST':
        form: SignUpForm = SignUpForm(
            request.POST, request.FILES, instance=user)

        if form.is_valid():
            user: User = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form: SignUpForm = SignUpForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})
