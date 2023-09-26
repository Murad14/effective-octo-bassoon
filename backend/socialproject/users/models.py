from django.db import models
from .api.models import Profile
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Assuming you have a User model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Other fields specific to your UserProfile model