from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpRequest

def logout_redirect(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('home')