from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages

from ..forms import LogInForm
from ..models import User
from ..helpers import login_prohibited

@login_prohibited
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: LogInForm = LogInForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data['username']
            password: str = form.cleaned_data['password']
            user: User = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                redirect_url: str = request.POST.get('next') or 'feed'
                return redirect(redirect_url)

        # Add error messages
        messages.add_message(request, messages.ERROR, "The username or password is incorrect") 

    form: LogInForm = LogInForm()

    # dealing with getting next redirect for required login page
    next: str = request.GET.get('next') or ''

    return render(request, 'login.html', {'form': form, 'next':next})