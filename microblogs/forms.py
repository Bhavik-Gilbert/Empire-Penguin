from django.core.validators import RegexValidator, MinLengthValidator
from django import forms
from .models import User, Post
import base64
from PIL import Image
import io

class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'profile_pic']
        widgets = { 'bio': forms.Textarea() }
    
    new_password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(),
        # Custom validator object
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain uppercase character, a lowercase character and a number'
            )
        ]
    )
    password_confirmation = forms.CharField(
        label='Password Confirmation', 
        widget=forms.PasswordInput()
    )

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Passwords do not match')

    def save(self):
        super().save(commit=False)

        user = User.objects.create_user(
            username = self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            profile_pic = self.cleaned_data.get('profile_pic'),
            password = self.cleaned_data.get('new_password')
        )

        return user
    
class PostForm(forms.ModelForm):
    """ Form to ask user for post text.The post author must be by the post creator."""

    class Meta:
        """Form options."""

        model = Post
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(),
        }
    
    def save(self, user, instance=None):
        super().save(commit=False)

        if instance is None:
            post = Post.objects.create(
                author = user, 
                text = self.cleaned_data.get('text'),
                image = self.cleaned_data.get('image')
                )
        else:
            post = self.instance
            post.text = self.cleaned_data.get("text")
            post.image = self.cleaned_data.get('image')
            post.save()

        return post
    
class SearchUserForm(forms.Form):
    """ Form to ask user for post text.The post author must be by the post creator."""

    search = forms.CharField(label='', required=False)