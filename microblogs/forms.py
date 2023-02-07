from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django import forms
from .models import User, Post


class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        self.current_user: int = kwargs.get("instance") or None
        super(SignUpForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'profile_pic']
        widgets = {'bio': forms.Textarea()}

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
        label='Password Confirmation/ New Password',
        widget=forms.PasswordInput()
    )

    def clean(self):
        super().clean()

        if self.current_user is None:
            new_password = self.cleaned_data.get('new_password')
            password_confirmation = self.cleaned_data.get(
                'password_confirmation')

            if new_password != password_confirmation:
                self.add_error(
                    'password_confirmation',
                    'Passwords do not match')
        else:
            new_password: str = self.cleaned_data.get('new_password')
            password_confirmation: str = self.cleaned_data.get(
                'password_confirmation')

            user = self.current_user
            user_login: User = authenticate(
                username=user.username, password=new_password)
            if user_login is None:
                self.add_error('new_password',
                               'Could not authenticate, incorrect password')

    def save(self):
        super().save(commit=False)

        if self.current_user is None:
            user = User.objects.create_user(
                username=self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                bio=self.cleaned_data.get('bio'),
                profile_pic=self.cleaned_data.get('profile_pic'),
                password=self.cleaned_data.get('new_password')
            )
        else:
            print(self.cleaned_data.get('profile_pic'))
            user: User = self.current_user
            user.username: str = self.cleaned_data.get('username')
            user.first_name: str = self.cleaned_data.get('first_name')
            user.last_name: str = self.cleaned_data.get('last_name')
            user.email: str = self.cleaned_data.get('email')
            user.bio: str = self.cleaned_data.get('bio')
            user.profile_pic: forms.ImageField = self.cleaned_data.get(
                'profile_pic')
            user.set_password(self.cleaned_data.get('new_password'))
            user.save()

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
                author=user,
                text=self.cleaned_data.get('text'),
                image=self.cleaned_data.get('image')
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
