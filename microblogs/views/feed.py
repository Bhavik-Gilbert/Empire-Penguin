from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from ..models import User, Following

@login_required
def feed_view(request: HttpRequest) -> HttpResponse:
    current_user: User = request.user
    feed_posts = []

    for following_id in current_user.get_following():
        following = User.objects.get(id=following_id)
        feed_posts += following.get_posts()
    
    feed_posts.sort(key=lambda x: x.created_at, reverse=True)

    return render(request, 'feed.html', {'feed_posts':feed_posts})