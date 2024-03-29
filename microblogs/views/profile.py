from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..models import User, Following


@login_required
def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    account_user: User = User.objects.filter(username=username)
    if len(account_user) != 1:
        return redirect('feed')

    account_user = User.objects.get(username=username)

    return render(request, "profile.html", {
                  'account_user': account_user, 'page': 'profile'})


@login_required
def follow_redirect(request: HttpRequest, page: str,
                    username: str) -> HttpResponse:
    current_user: User = request.user
    account_user: User = User.objects.filter(username=username)

    if len(account_user) == 1:  # Checks there's only one user
        account_user = User.objects.get(username=username)
        already_following = Following.objects.filter(
            follower=current_user, following=account_user)
        # Stops users from following themselves or someone they already follow
        if account_user != current_user and len(already_following) == 0:
            Following.objects.create(
                follower=current_user,
                following=account_user
            )

    try:
        return redirect(page, username)
    except BaseException:
        return redirect(page)


@login_required
def unfollow_redirect(request: HttpRequest, page: str,
                      username: str) -> HttpResponse:
    current_user: User = request.user
    account_user: User = User.objects.filter(username=username)

    if len(account_user) == 1:  # Checks there's only one user
        account_user = User.objects.get(username=username)
        find_unfollow: list[Following] = Following.objects.filter(
            follower=current_user, following=account_user)
        if len(find_unfollow) > 0:  # Deletes all records of following
            find_unfollow.delete()

    try:
        return redirect(page, username)
    except BaseException:
        return redirect(page)
