# Generated by Django 5.1.3 on 2024-12-06 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_condizionipagamento_codpag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condizionipagamento',
            name='codpag',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
