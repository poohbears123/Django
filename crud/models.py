from django.db import models
from django.contrib.auth.models import User

class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

# Optionally, if you want to extend User with additional fields, you can create a Profile model
# For simplicity, we will use the default User model for authentication and user data
