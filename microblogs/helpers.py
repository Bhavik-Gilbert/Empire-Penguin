from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q

from .models import User
from .forms import SearchUserForm


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def search_users(user_list: list[User], form: SearchUserForm):
    return user_list.filter(
                Q(username__icontains=form.cleaned_data.get("search"))
                | Q(first_name__icontains=form.cleaned_data.get("search"))
                | Q(last_name__icontains=form.cleaned_data.get("search"))
                | Q(email__icontains=form.cleaned_data.get("search"))
                )