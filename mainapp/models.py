from django.db import models
from django.contrib.auth.models import User

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='avatars/', null=True)
    
    def __str__(self):
        return self.user.username

