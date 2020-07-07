from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
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


class Item(models.Model):
    name = models.CharField(max_length=50)
    CATEGORIES = (
        ('Tools', 'Tools'),
        ('Clothes', 'Clothes'),
        ('Kitchen', 'Kitchen'),
        ('Bedclothes', 'Bedclothes'),
        ('Holidays', 'Holidays'),
        ('Bathroom', 'Bathroom'),
        ('Car_stuff', 'Car stuff'),
        ('Other', 'Other'),
    )
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50)
    is_borrowed = models.BooleanField(default=False, blank=True)
    who_borrowed = models.CharField(max_length=30, blank=True, default='')
    when_borrowed = models.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['name']

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.users.add(User.objects.get(self.user.id))

    def __str__(self):
        return f'{self.name}, category: {self.category}, location:'

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
