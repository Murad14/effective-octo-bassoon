from django.db import models
from .api.models import Profile
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  