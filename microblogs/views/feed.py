from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from ..forms import PostForm

@login_required
def feed_view(request: HttpRequest) -> HttpResponse:
    form: PostForm = PostForm()
    return render(request, 'feed.html', {'form': form})