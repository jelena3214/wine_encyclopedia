# Generated by Django 4.2.1 on 2023-06-01 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0004_merge_20230531_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termin',
            name='vreme',
            field=models.DateField(blank=True, null=True),
        ),
    ]