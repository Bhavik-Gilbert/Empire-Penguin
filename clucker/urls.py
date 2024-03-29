"""clucker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from microblogs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path(
        'edit_user_profile/',
        views.edit_user_profile_view,
        name='edit_user_profile'),
    path('feed/', views.feed_view, name='feed'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_redirect, name='logout'),
    path('new_post/', views.new_post_view, name='new_post'),
    path('find_users/', views.find_users_view, name='find_users'),
    re_path(
        r'profile/(?P<username>\w+)/$',
        views.profile_view,
        name='profile'),
    re_path(
        r'edit_post/(?P<pk>\d+)/(?P<username>\w+)/$',
        views.edit_post,
        name='edit_post'),
    re_path(r'delete_post/(?P<pk>\d+)/(?P<username>\w+)/$',
            views.delete_post_redirect, name='delete_post'),
    re_path(r'follow/(?P<page>\w+)/(?P<username>\w+)/$',
            views.follow_redirect, name='follow'),
    re_path(r'unfollow/(?P<page>\w+)/(?P<username>\w+)/$',
            views.unfollow_redirect, name='unfollow'),
    re_path(
        r'find_followers/(?P<username>\w+)/$',
        views.find_followers_view,
        name='find_followers')
]
