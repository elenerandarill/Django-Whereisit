# Generated by Django 3.0.7 on 2020-07-07 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whereisit_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('is_borrowed', models.BooleanField(default=False)),
                ('who_borrowed', models.CharField(blank=True, max_length=30)),
                ('when_borrowed', models.DateTimeField(blank=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]