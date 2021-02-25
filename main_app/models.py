from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.last_name} {self.last_name}"