from datetime import date
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class Users(AbstractUser):
    firstname = models.CharField(max_length=20, null=False)
    lastname = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=10, null=False, default='N/A')
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile = models.FileField(upload_to='profiles/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.username}"

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class Articles(models.Model):
    author = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    published = models.BooleanField(default=False)
    cover_image = models.FileField(upload_to='Articles/cover_images/', null=True)
    content_images  = models.FileField(upload_to='Articles/content_images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.author + " - " + self.title
    
class ArticleViews(models.Model):
    author = models.CharField(max_length=100, null=False)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} viewed {self.article} at {self.created_at}"


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