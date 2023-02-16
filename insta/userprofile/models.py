from django.db import models
from django.contrib.auth.models import User
from post.models import Post
# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="userprofile")
    favourite = models.ManyToManyField(Post)
    image = models.ImageField(upload_to="profile_pciture", null=True, default="default.jpg")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    
