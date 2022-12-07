from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpRequest

from ..models import Post, User

def delete_post_redirect(request: HttpRequest, pk: int, username:str) -> HttpResponseRedirect:
    current_user: User = request.user
    post:Post = Post.objects.filter(id=pk)

    if (len(post) == 1):
        post = Post.objects.get(id=pk)

        if (post.author == current_user):
            post.delete()

    return redirect('profile', username)