from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vegbox-details')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def register_details(request):
    if request.method == 'POST':
        form1 = ProfileForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request, f'Account has been created!')
            return redirect('login')
    else:
        form1 = ProfileForm()   
    return render(request, 'users/register_details.html', {'form': form1})
     
     