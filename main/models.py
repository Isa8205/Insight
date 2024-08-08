from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class Users(AbstractUser):
    full_name = models.CharField(max_length=50, null=False)
    profile = models.FileField(upload_to='profiles/', null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.full_name + '-' + self.username


class Articles(models.Model):
    author = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.author + " - " + self.title


class Comments(models.Model):
    author = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.author + '-' + self.content


class SiteReviews(models.Model):
    content = models.TextField(null=False)
    author = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.author + '-' + self.content
    
class Likes(models.Model):
    author = models.CharField(max_length=100, null=False)
    article = models.CharField(max_length=100, null=False)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Likes'

    def __str__(self):
        return '{author} liked {article} at {time}'
    
class Dislikes(models.Model):
    author = models.CharField(max_length=100, null=False)
    article = models.CharField(max_length=100, null=False)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Likes'

    def __str__(self):
        return '{author} disliked {article} at {time}'