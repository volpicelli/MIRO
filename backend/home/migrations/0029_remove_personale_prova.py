# Generated by Django 5.1.4 on 2024-12-22 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_personale_prova'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personale',
            name='prova',
        ),
    ]
