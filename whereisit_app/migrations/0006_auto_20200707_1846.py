# Generated by Django 3.0.7 on 2020-07-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whereisit_app', '0005_auto_20200707_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Tools', 'Tools'), ('Clothes', 'Clothes'), ('Kitchen', 'Kitchen'), ('Bedclothes', 'Bedclothes'), ('Holidays', 'Holidays'), ('Bathroom', 'Bathroom'), ('Car stuff', 'Car stuff'), ('Other', 'Other')], max_length=20),
        ),
    ]