# Generated by Django 5.1.2 on 2024-10-31 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='image',
            field=models.ImageField(upload_to='documents/'),
        ),
    ]
