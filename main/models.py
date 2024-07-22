from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class Users(models.Model):
    full_name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=16, null=False)
    profile = models.FileField(upload_to='profiles/', null=True)

    USERNAME_FIELD = 'username'

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
    content = models.TextField(null=False)
    author = models.CharField(max_length=100, null=False)
    article = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.author + '-' + self.content


class Reviews(models.Model):
    content = models.TextField(null=False)
    author = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.author + '-' + self.content
