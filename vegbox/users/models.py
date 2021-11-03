from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    number = models.CharField(max_length=10)