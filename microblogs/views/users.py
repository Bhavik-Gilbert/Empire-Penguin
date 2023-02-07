from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..models import User
from ..forms import SearchUserForm
from ..helpers import search_users


@login_required
def find_users_view(request: HttpRequest) -> HttpResponse:
    current_user: User = request.user
    form: SearchUserForm = SearchUserForm()
    account_list: list[User] = User.objects.exclude(id=current_user.id)

    if request.method == 'POST':
        form = SearchUserForm(request.POST)
        if form.is_valid():
            account_list = search_users(account_list, form)

    return render(request, "find_users.html", {
                  'form': form, 'account_list': account_list, 'page': 'find_users'})


def find_followers_view(request: HttpRequest, username: str) -> HttpResponse:
    account_user: list[User] = User.objects.filter(username=username)

    if len(account_user) == 1:
        account_user: User = User.objects.get(username=username)
        form: SearchUserForm = SearchUserForm()
        account_list: list[User] = account_user.get_followers()

        if request.method == 'POST':
            form = SearchUserForm(request.POST)
            if form.is_valid():
                follower_list: list[User] = account_list
                account_list = []
                for user in follower_list:
                    user_account = User.objects.filter(id=user.id)
                    account_list = [*account_list, *
                                    search_users(user_account, form)]

        return render(request, "find_users.html", {
                      'form': form, 'account_list': account_list, 'page': 'find_followers'})

    return redirect('feed')
