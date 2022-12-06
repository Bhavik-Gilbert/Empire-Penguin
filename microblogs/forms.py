from django.core.validators import RegexValidator
from django import forms
from .models import User, Post

class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
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
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            password = self.cleaned_data.get('new_password'),
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
            'image': forms.ClearableFileInput()
        }
    
    def save(self, user):
        super().save(commit=False)

        post = Post.objects.create(
            author=user, 
            text=self.cleaned_data.get('text'))

        return post