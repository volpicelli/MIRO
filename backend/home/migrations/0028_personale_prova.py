# Generated by Django 5.1.4 on 2024-12-22 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_fornitori_azienda'),
    ]

    operations = [
        migrations.AddField(
            model_name='personale',
            name='prova',
            field=models.ManyToManyField(to='home.cantiere'),
        ),
    ]