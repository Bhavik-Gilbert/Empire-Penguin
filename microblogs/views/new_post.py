from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from ..forms import PostForm
from ..models import User


@login_required
def new_post_view(request: HttpRequest) -> HttpResponse:
    form: PostForm = PostForm()

    if request.method == 'POST':
        current_user: User = request.user
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(current_user)
            return redirect('feed')

    return render(request, 'new_post.html', {'form': form})
