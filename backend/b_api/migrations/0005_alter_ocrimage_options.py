# Generated by Django 5.1.2 on 2024-11-06 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b_api', '0004_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ocrimage',
            options={'ordering': ['-uploaded_at']},
        ),
    ]
