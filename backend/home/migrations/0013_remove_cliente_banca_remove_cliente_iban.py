# Generated by Django 5.1.3 on 2024-12-12 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_azienda_banca_azienda_cap_azienda_cellulare_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='banca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='iban',
        ),
    ]
