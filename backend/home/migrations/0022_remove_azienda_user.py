# Generated by Django 5.1.4 on 2024-12-18 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_usersazienda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='azienda',
            name='user',
        ),
    ]