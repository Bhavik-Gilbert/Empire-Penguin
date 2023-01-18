from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser

import random
import string
import os

"""Function to rename image files"""
def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(''.join(random.choice(string.ascii_letters) for i in range(48)), ext)
    # return the whole path to the file
    return os.path.join('static/media_files', filename)

class User(AbstractUser):
    """Users in microblogs"""

    username = models.CharField(
        max_length=30, 
        unique=True,
        # Custom validator object
        validators=[RegexValidator(
            regex=r'^\w{3,}$',
            message='Username must consist of at least three alphanumericals'
        )]
    )
    
    profile_pic = models.ImageField(upload_to=wrapper, blank=True)

    first_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    last_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    email = models.EmailField(
        unique=True,
        blank=False
    )

    bio = models.CharField(
        max_length=520,
        blank=True,
        unique=False
    )

    def __str__(self):
        return str(self.username)
     
    def get_posts(self):
        return Post.objects.filter(author=self)
    
    def get_followers(self):
        followers_id: list[int] = Following.objects.filter(following=self).values_list('follower', flat=True)
        followers: list[User] = []

        for user_id in followers_id:
            followers.append(User.objects.get(id=user_id))
        
        return followers

    def get_following(self):
        following_id = Following.objects.filter(follower=self).values_list('following', flat=True)
        following: list[User] = []

        for user_id in following_id:
            following.append(User.objects.get(id=user_id))
        
        return following

class Post(models.Model):
    """Posts by users in their microblogs"""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(
        max_length=280,
        validators=[MinLengthValidator(
            limit_value=1,
            message="Why would you want to post an empty message"
        )]
        )

    image = models.ImageField(upload_to=wrapper, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model options."""

        ordering = ['-created_at']


class Following(models.Model):
    """Holds data of who Users follow"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower') # User who is following other user
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') # User they are following