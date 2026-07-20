from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from django_extensions.db.fields import AutoSlugField 

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
    
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_extensions.db.fields import AutoSlugField

#  it gives us our active user model here in settings we have
#  mentioned our User model so it takes form there .
User = get_user_model()

class Tag(models.Model):

    name = models.CharField(max_length=100)

    slug = AutoSlugField(
        populate_from="name",
        unique=True
    )

    def __str__(self):
        return self.name
    



class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = AutoSlugField(
        populate_from="name",
        unique=True
    )

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,

        # without it django default category_objects.post_set.all()
        #  now we can have category_objects.posts.all()
        related_name="posts",
        
    )


    title = models.CharField(max_length=200)

    slug = AutoSlugField(
        populate_from="title",
        unique=True
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
        null=True
    )

    featured_image = models.ImageField(
        upload_to="featured_images/",
        blank=True,
        null=True
    )


    text = models.TextField()

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    published_date = models.DateTimeField(
        blank=True,
        null=True
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Comment(models.Model):

    # ab apn isme Post model ke obj se us particular post obj
    #  ke sare comments find kar sakthe hai 
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    def __str__(self):

        return f"{self.author.username} - {self.post.title}"


