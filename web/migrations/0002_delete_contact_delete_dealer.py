# Generated by Django 4.1.9 on 2024-09-01 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Dealer',
        ),
    ]