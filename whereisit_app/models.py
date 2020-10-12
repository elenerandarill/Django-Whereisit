from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from PIL import Image

from .choices import CATEGORIES, LOCATIONS, PLACES, GROUPS


class GroupOfUsers(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'group: {self.name}'


class User(AbstractUser):
    u_groups = models.ManyToManyField(GroupOfUsers)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # TUTAJ

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save()


class Location(models.Model):
    room = models.CharField(max_length=50)
    furniture = models.CharField(max_length=100)
    position_x = models.IntegerField(help_text='value in pixels')
    position_y = models.IntegerField(help_text='value in pixels')

    def __str__(self):
        return f"{self.room}, {self.furniture}."


class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='def-item.png', upload_to='items_pics')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, models.SET_NULL, blank=True, null=True)
    is_borrowed = models.BooleanField(default=False, blank=True)
    who_borrowed = models.CharField('If yes, who has borrowed it:', max_length=30, blank=True, default='')
    when_borrowed = models.DateTimeField('If yes, then when was that(YYYY-MM-DD):', null=True, blank=True)
    groups = models.ManyToManyField(GroupOfUsers)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'id:{self.id}, {self.name}, category: {self.category}.'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
