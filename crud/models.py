from django.db import models
from django.contrib.auth.models import User

class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
