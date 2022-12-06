from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpRequest

from ..forms import PostForm
from ..models import User


@login_required
def new_post_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user: User = request.user
            form: PostForm = PostForm(request.POST)
            if form.is_valid():
                form.save(current_user)
                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
