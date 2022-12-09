from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser

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
    
    profile_pic = models.TextField(blank=True, null=True)

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
        return Following.objects.filter(following=self).values_list('follower', flat=True)

    def get_following(self):
        return Following.objects.filer(follower=self).values_list('following', flat=True)


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

    image = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model options."""

        ordering = ['-created_at']


class Following(models.Model):
    """Holds data of who Users follow"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower') # User who is following other user
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') # User they are following