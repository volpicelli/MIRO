# Generated by Django 5.1.3 on 2024-12-06 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condizionipagamento',
            old_name='codpag_id',
            new_name='codpag',
        ),
    ]