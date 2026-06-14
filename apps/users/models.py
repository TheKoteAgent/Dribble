from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    website = models.URLField(blank=True, max_length=255)
    twitter = models.URLField(blank=True, max_length=255)
    instagram = models.URLField(blank=True, max_length=255)
    linkedin = models.URLField(blank=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f"{self.username} ({self.email})"