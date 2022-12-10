from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from ..forms import PostForm
from ..models import User, Post


@login_required
def new_post_view(request: HttpRequest) -> HttpResponse:
    form: PostForm = PostForm()

    if request.method == 'POST':
        current_user: User = request.user
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(current_user)
            return redirect('feed')

    return render(request, 'post.html', {'form': form})

def edit_post(request: HttpRequest, pk: int, username: str) -> HttpResponseRedirect:
    current_user: User = request.user
    post:Post = Post.objects.filter(id=pk)

    if (len(post) == 1):
        post = Post.objects.get(id=pk)
        form: PostForm = PostForm(instance=post)

        if request.method == 'POST':
            current_user: User = request.user
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save(current_user, post)
                return redirect('profile', username)
    else:
        return redirect('profile', username)

    return render(request, 'post.html', {'form': form})

def delete_post_redirect(request: HttpRequest, pk: int, username: str) -> HttpResponseRedirect:
    current_user: User = request.user
    post:Post = Post.objects.filter(id=pk)

    if (len(post) == 1):
        post = Post.objects.get(id=pk)

        if (post.author == current_user):
            post.delete()

    return redirect('profile', username)