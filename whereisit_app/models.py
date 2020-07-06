from django.contrib.auth.models import User
from django.db import models
from PIL import Image


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


# class Item(models.Model):
#     name = models.CharField(max_length=50)
#     category = models.CharField(max_length=30)
#     description = models.TextField()
#     location = models.CharField()
#     is_borrowed = models.BooleanField(default=False)
#     who_borrowed = models.CharField(max_length=30)
#     when_borrowed = models.DateTimeField()
#     owners = models.ManyToManyField(User)
#
#     class Meta:
#         ordering = ['name']
#
#     def __str__(self):
#         return f'{self.name}, category: {self.category}, location:'
