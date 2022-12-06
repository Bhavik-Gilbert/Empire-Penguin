from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..forms import SignUpForm
from ..models import User
from ..helpers import login_prohibited


@login_prohibited
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: SignUpForm = SignUpForm(request.POST)

        if form.is_valid():
            user: User = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form: SignUpForm = SignUpForm()
       
    return render(request, 'signup.html', {'form': form})