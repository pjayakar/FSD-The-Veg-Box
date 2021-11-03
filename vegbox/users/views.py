from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('vegbox-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def createprofile(request):
    
    user_ = User.objects.get(pk=1)
    profile = Profile(user=user_)
    profile.user.first_name = 'Joe'
    profile.user.last_name = 'Soe'
    profile.user.email = 'Joe@Soe.com'
    profile.user.save()
    profile.save()