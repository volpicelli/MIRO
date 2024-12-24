# Generated by Django 5.1.4 on 2024-12-18 22:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_remove_azienda_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersazienda',
            name='azienda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aziendauser', to='home.azienda'),
        ),
        migrations.AlterField(
            model_name='usersazienda',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userazienda', to=settings.AUTH_USER_MODEL),
        ),
    ]