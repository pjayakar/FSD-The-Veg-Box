from django.shortcuts import render
from django.http import HttpResponse, response

# Create your views here.
def home(request):
    return render(request,'vegbox_app/home.html')
def fruits(request):
    return render(request,'vegbox_app/fruits.html')

def dairy(request):
    return render(request,'vegbox_app/dairy.html')
