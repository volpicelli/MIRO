# Generated by Django 5.1.3 on 2024-12-09 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_dummy_magazzino_quantita_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articoli',
            name='nome',
        ),
    ]