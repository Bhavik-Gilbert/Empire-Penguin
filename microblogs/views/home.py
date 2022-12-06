from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from ..helpers import login_prohibited

@login_prohibited
def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')