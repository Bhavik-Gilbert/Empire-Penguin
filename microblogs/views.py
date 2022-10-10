from django.shortcuts import render

from .forms import SignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})