# Generated by Django 4.2 on 2023-05-23 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0003_muzika_ostalo_pozoriste_sport_zurka'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='muzika',
            table='muzika',
        ),
        migrations.AlterModelTable(
            name='ostalo',
            table='ostalo',
        ),
        migrations.AlterModelTable(
            name='pozoriste',
            table='pozoriste',
        ),
        migrations.AlterModelTable(
            name='sport',
            table='sport',
        ),
        migrations.AlterModelTable(
            name='zurka',
            table='zurka',
        ),
    ]