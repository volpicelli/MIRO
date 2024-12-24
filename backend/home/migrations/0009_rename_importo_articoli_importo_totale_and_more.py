# Generated by Django 5.1.3 on 2024-12-10 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_articoli_nome'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articoli',
            old_name='importo',
            new_name='importo_totale',
        ),
        migrations.RenameField(
            model_name='ordine',
            old_name='magazzino',
            new_name='mestesso',
        ),
        migrations.RemoveField(
            model_name='magazzino',
            name='articolo',
        ),
        migrations.AddField(
            model_name='articoli',
            name='prezzo_unitario',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='magazzino',
            name='descrizione',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='magazzino',
            name='importo_totale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='magazzino',
            name='prezzo_unitario',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]