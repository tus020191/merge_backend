from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    city = models.CharField(max_length=200, blank=True,null=True)
    state = models.CharField(max_length=100, blank=True,null=True)
    phone_no = models.CharField(max_length=15, blank=True,null=True)
    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
    

class Post(models.Model):
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    title          = models.CharField(max_length=200)
    text           = models.TextField()
    created_date   = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    


