# Generated by Django 4.2.1 on 2023-06-05 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0007_alter_rezultatupitnika_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rezultatupitnika',
            unique_together=set(),
        ),
    ]
