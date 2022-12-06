from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..models import User


@login_required
def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    account_user: User = User.objects.filter(username=username)
    if len(account_user) != 1:
        return redirect('feed')

    account_user = User.objects.get(username=username)
    
    return render(request, "profile.html", {'posts': account_user.get_posts()})


    