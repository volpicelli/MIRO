# Generated by Django 5.1.4 on 2024-12-24 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_alter_documenti_options_alter_documenti_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='codcf',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='fornitori',
            name='codcf',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
    ]